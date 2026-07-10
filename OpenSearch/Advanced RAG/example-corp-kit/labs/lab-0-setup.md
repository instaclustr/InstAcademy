# Lab 0: Setup (before Chapter 1)

**Time:** ~20 minutes.
**You need:** an OpenSearch 3.x cluster URL with credentials (Instaclustr
Managed Platform with the AI Search add-on, or your own 3.1+ cluster;
the course targets 3.6+), a terminal with `curl` and `python3`
(standard library only, nothing to pip install), and this course kit.

**What you're building across all labs:** the internal AI support tool
for Example Corp, a BI platform whose support team handles 500 tickets a
day. Every lab adds a layer to the same system, so do the labs in order:
0, 1, 2, 3, 4.

**How these labs work:** every step is copy-paste. Each step tells you
what you are doing, why it matters, and exactly what you should see.
If what you see does not match, stop and fix it before moving on;
later labs depend on earlier state.

---

## Step 1: Point your shell at the cluster

**What you're doing:** storing the cluster URL (with credentials) in an
environment variable that every command in every lab reads.

```bash
export OS_URL=https://USER:PASS@your-cluster:9200
```

**Why:** credentials live in your shell session, never in files, never
in git, never in the lab documents. Close the terminal and they are
gone. If you open a new terminal later, re-export `OS_URL` (and
`MODEL_ID` from Step 4) before continuing.

Now prove the cluster is reachable:

```bash
curl -s "$OS_URL" | python3 -m json.tool
```

**Expected result:** a JSON block including
`"distribution": "opensearch"` and a `version.number` of 3.1 or higher:

```json
{
  "name": "...",
  "cluster_name": "...",
  "version": {
    "distribution": "opensearch",
    "number": "3.5.0",
    ...
  }
}
```

**Checkpoint 0.1:** `version.number` is 3.1+ and the distribution says
`opensearch`. If you get a certificate error on a dev cluster, note it
and ask your instructor; do not disable TLS verification casually.

## Step 2: Verify the course corpus

**What you're doing:** extracting the canonical Example Corp data batch
and proving it is byte-identical to the one used to record the course.

```bash
cd corpus
tar xzf example-corp-corpus-v2.1.0.tar.gz
cd ..
python3 scripts/verify_corpus.py --corpus corpus/example-corp-corpus-v2.1.0
```

**Why:** every learner works from the same batch of synthetic Example
Corp data. The verify script checks every file against a sha256
manifest. When your eval numbers in Lab 1 land within a whisker of the
course's reference numbers, that is not luck: same data, same model,
same math (Lab 1 explains the whisker). If verification fails,
re-download the tarball; never regenerate locally.

**Expected result:**

```
example-corp-corpus v2.1.0 (built 2026-07-05T14:56:52+00:00)
OK: 1072 files verified. 8955 chunks, 300 golden queries, 10000 tickets.
```

**Checkpoint 0.2:** the output ends with `OK: 1072 files verified.`

## Step 3: Create the model group

**What you're doing:** creating the container that will hold every
version of the course embedding model.

```bash
curl -s -X POST "$OS_URL/_plugins/_ml/model_groups/_register" \
  -H 'Content-Type: application/json' -d '{
  "name": "support-embedding-models",
  "description": "Embedding models for the Example Corp support tool labs"
}'
```

**Why:** lesson 1.4 treats an embedding model change as a schema
migration. Model groups are the machinery that makes that discipline
real: every model version registers into a group, so "which model
embedded this index" always has an answer.

**Expected result:**

```json
{"model_group_id":"<some id>","status":"CREATED"}
```

Copy the `model_group_id` value; the next step needs it.

## Step 4: Register and deploy the course embedding model

**What you're doing:** registering
`huggingface/sentence-transformers/all-MiniLM-L6-v2`, the standard
course model. It runs *inside* the cluster on the ML nodes, so the labs
need no external API keys.

Paste your `model_group_id` into this command, then run it:

```bash
curl -s -X POST "$OS_URL/_plugins/_ml/models/_register" \
  -H 'Content-Type: application/json' -d '{
  "name": "huggingface/sentence-transformers/all-MiniLM-L6-v2",
  "version": "1.0.2",
  "model_group_id": "<MODEL_GROUP_ID from Step 3>",
  "model_format": "TORCH_SCRIPT"
}'
```

**Expected result:** `{"task_id":"<some id>","status":"CREATED"}`.
Registration downloads the model onto the cluster, which takes a minute
or two. Poll the task (paste your `task_id`) until `state` is
`COMPLETED`:

```bash
curl -s "$OS_URL/_plugins/_ml/tasks/<TASK_ID>" | python3 -m json.tool
```

**Expected result (when done):** `"state": "COMPLETED"` and a
`model_id` field. That `model_id` is the single most important value in
the whole course: it defines your vector space. Save it in your shell:

```bash
export MODEL_ID=<model_id from the completed task>
```

Now deploy it into memory on the ML nodes:

```bash
curl -s -X POST "$OS_URL/_plugins/_ml/models/$MODEL_ID/_deploy"
```

Give it ~30 seconds, then check:

```bash
curl -s "$OS_URL/_plugins/_ml/models/$MODEL_ID" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['model_state'])"
```

**Expected result:** `DEPLOYED`.

**If you see `PARTIALLY_DEPLOYED`:** the model loaded on some ML nodes
but at least one node's memory circuit breaker was open. The model
still works (Step 5 will prove it). Re-run the `_deploy` call once to
pick up the remaining node; if it stays partial on a busy shared
cluster, note it and continue.

**Why this exact model:** every index mapping in the labs uses 384
dimensions, and the course's published eval numbers were produced with
this model. A different model still works mechanically, but your Lab 1
metrics will differ from the video. Lesson 1.1 told you why: the model
defines the vector space, and ingest and query must live in the same
one.

## Step 5: Prove the model answers

**What you're doing:** sending one sentence through the deployed model
and looking at what comes back.

```bash
curl -s -X POST "$OS_URL/_plugins/_ml/_predict/text_embedding/$MODEL_ID" \
  -H 'Content-Type: application/json' \
  -d '{"text_docs":["connector handshake failed"],"return_number":true,"target_response":["sentence_embedding"]}' \
  | python3 -c "import sys,json; o=json.load(sys.stdin)['inference_results'][0]['output'][0]; print('dimensions:', o['shape'][0]); print('first 3 values:', o['data'][:3])"
```

**Expected result:**

```
dimensions: 384
first 3 values: [-0.048449516, -0.019668244, 0.025217716]
```

Your three values should match those exactly: same model, same text,
same vector, on your cluster and everyone else's. That determinism is
the foundation the whole course's "your numbers match the video"
promise stands on.

**Checkpoint 0.3:** the predict returns a 384-dimension vector.

**If registration was blocked** by a cluster setting (common on managed
platforms without ML-capable nodes), your instructor will provide
either the setting to request or a remote connector recipe
(`kit/code-samples/lesson-1-4.md`). Do not change cluster settings on a
shared cluster.

## Step 6: Connect a real LLM (the primary path)

**What you're doing:** connecting a generative model to the cluster
through an ML Commons connector, so the later labs can run query
rewriting, HyDE, grading, and full RAG answers against a real LLM. This
is lesson 1.4's connector pattern, for real: the credential lives
encrypted in the connector, one endpoint, one model, least privilege.

**Get a free API key from either provider** (both are free, no credit
card, and both endpoints are pre-trusted on the Instaclustr platform;
pick whichever you can sign up for fastest):

- **Cohere:** https://dashboard.cohere.com/api-keys (create an account,
  copy the Trial key)
- **Google Gemini:** https://aistudio.google.com/apikey (any Google
  account)

> **Two notes on free tiers.** First, free tiers may use your inputs to
> improve the provider's products; that is fine here because the
> Example Corp corpus is synthetic and public by design. Never point a
> free-tier key at private data. Second, free-tier requests are served
> at lower priority and capped per minute: an occasional
> `429 rate limited`, `503 high demand`, or (Cohere)
> `NO_VALID_RESPONSE_GENERATED` is normal; wait a minute and re-run the
> command. We hit these during validation too; every one cleared on
> retry.

Put the key in your shell (like `OS_URL`, it lives here and nowhere
else):

```bash
export LLM_KEY=<your key>
```

Create the connector for YOUR provider. **Cohere:**

```bash
curl -s -X POST "$OS_URL/_plugins/_ml/connectors/_create" -H 'Content-Type: application/json' -d '{
  "name": "support-llm-cohere",
  "description": "Cohere for the support tool labs. One endpoint, one model.",
  "version": 1,
  "protocol": "http",
  "parameters": { "model": "command-a-03-2025" },
  "credential": { "llm_key": "'$LLM_KEY'" },
  "actions": [{
    "action_type": "predict",
    "method": "POST",
    "url": "https://api.cohere.ai/v2/chat",
    "headers": { "Authorization": "Bearer ${credential.llm_key}",
                 "Content-Type": "application/json" },
    "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": [{\"role\": \"user\", \"content\": \"${parameters.prompt}\"}], \"temperature\": 0 }"
  }]
}'
```

**Or Gemini:**

```bash
curl -s -X POST "$OS_URL/_plugins/_ml/connectors/_create" -H 'Content-Type: application/json' -d '{
  "name": "support-llm-gemini",
  "description": "Gemini for the support tool labs. One endpoint, one model.",
  "version": 1,
  "protocol": "http",
  "parameters": { "model": "gemini-flash-latest" },
  "credential": { "llm_key": "'$LLM_KEY'" },
  "actions": [{
    "action_type": "predict",
    "method": "POST",
    "url": "https://generativelanguage.googleapis.com/v1beta/models/${parameters.model}:generateContent",
    "headers": { "x-goog-api-key": "${credential.llm_key}",
                 "Content-Type": "application/json" },
    "request_body": "{ \"contents\": [{\"parts\":[{\"text\":\"${parameters.prompt}\"}]}], \"generationConfig\": {\"temperature\": 0} }"
  }]
}'
```

**If the create returns a 500 mentioning `Fetching master key timed
out`:** that is the cluster initializing its credential-encryption key
on first use; run the same command once more and it succeeds.

**Why this shape:** the key is stored encrypted by ML Commons and never
appears in your application code or query bodies again. The connector
can reach exactly one host and one model, so it cannot accidentally
reach anywhere else. `temperature: 0` minimizes (but does not
eliminate) run-to-run variation. And both endpoints are on the
Instaclustr platform's pre-trusted connector list, so no cluster
settings change. Every LLM command in Labs 2-4 is identical regardless
of which provider you chose; a small helper (`scripts/llm_text.py`)
reads either provider's response shape.

**Expected result:** `{"connector_id":"<some id>"}`. Now register it as
a remote model and deploy (paste your `connector_id`):

```bash
curl -s -X POST "$OS_URL/_plugins/_ml/models/_register" -H 'Content-Type: application/json' -d '{
  "name": "support-llm",
  "function_name": "remote",
  "description": "Generative model for the support tool labs",
  "connector_id": "<CONNECTOR_ID from above>"
}'
```

**Expected result:** a completed registration with a `model_id` (remote
models register instantly; if you get a `task_id` instead, poll it as
in Step 4). Save and deploy it:

```bash
export LLM_ID=<model_id from the registration>
curl -s -X POST "$OS_URL/_plugins/_ml/models/$LLM_ID/_deploy"
```

(Remote models sometimes report `PARTIALLY_DEPLOYED`, same as Step 4
explained for the embedding model; the checkpoint below is what
matters.)

**Checkpoint 0.4:** the LLM answers through the cluster:

```bash
curl -s -X POST "$OS_URL/_plugins/_ml/models/$LLM_ID/_predict" \
  -H 'Content-Type: application/json' \
  -d '{"parameters":{"prompt":"Reply with exactly the word: connected"}}' \
  | python3 scripts/llm_text.py
```

Expected: `connected`

> **The variance caveat, once, for the whole course.** Wherever a lab
> shows LLM output from here on, it shows what WE got on the run we
> validated. Your output will differ in wording, across models, model
> versions, and even runs at temperature 0. That is not a failed
> checkpoint. LLM checkpoints in these labs always name the *behavior*
> that must hold (e.g. "the rewrite restores the error code and the
> topic"), and the sample output is there so you know roughly what
> good looks like. The deterministic parts of the course (retrieval
> scores, counts, eval metrics) keep their exact expectations.

**No key, or no interest in one?** Every LLM step in Labs 2-4 has a
marked **"No-LLM alternative"** where you perform the model's job by
hand with pre-written text. You get identical retrieval results and
identical checkpoints; you just don't see a live model produce the
intermediate text. Skip this step and use those boxes.

---

**You are ready when:** Checkpoints 0.1-0.3 pass (and 0.4 if you are on
the LLM path). Keep this shell open (or remember to re-export `OS_URL`,
`MODEL_ID`, and `LLM_ID`); Lab 1 starts by ingesting the corpus.
