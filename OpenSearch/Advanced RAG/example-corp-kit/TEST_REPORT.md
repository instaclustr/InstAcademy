# TEST_REPORT.md: Example Corp Kit Validation

**Validation run 2 (LLM path, post-fixes).** Executed 2026-07-10 as a
first-time learner would: labs run literally, in order, from the kit
root, on a completely wiped cluster (no prior support-* resources,
models, or connectors). Primary (LLM) path throughout: Lab 0 Step 6
with the **Cohere** provider (`command-a-03-2025`), Lab 2 LLM rewrite
and HyDE steps, Lab 3 Step 4b, Lab 4 Step 9.

## Environment

| | |
| --- | --- |
| Cluster | OpenSearch **3.5.0** (distribution: opensearch), 7 nodes (3× data+ingest+ml 1.9 GB heap, 3× master, 1× coordinator) |
| Health | green before, during (spot-checked), and after all heavy phases |
| Plugins | opensearch-knn, opensearch-ml, opensearch-neural-search, opensearch-index-management, all 3.5.0.0, all nodes |
| Feature gates | hybrid/normalization (2.10+) OK; score-ranker RRF (2.19+) OK; Memory API (2.12+) OK; neural `filter` param (2.13+) OK. 3.6-only features (agentic memory, token tracking, BBQ) not exercised, Lab 4 Step 8 correctly flags token tracking as a 3.6 feature in prose only. |
| Corpus | example-corp-corpus v2.1.0, `OK: 1072 files verified. 8955 chunks, 300 golden queries, 10000 tickets.` (one ignored `.DS_Store` extra noted by the verifier) |
| LLM | Cohere trial key via ML Commons connector, remote model `support-llm` |

## Overall result

**All five labs PASS on the primary LLM path.** 30 checkpoints
executed: **28 PASS, 0 FAIL, 2 PASS-with-note** (both numeric-drift
notes, below). Every LLM behavioral checkpoint met its behavior
contract on the first response, no retry was ever needed for an LLM
*predict* call. One transient cluster-side error during connector
creation cleared on a single retry.

## Per-lab wall time

| Lab | Stated budget | Observed | Verdict |
| --- | --- | --- | --- |
| 0 | ~20 min | ~9 min (model registration completed in ~30 s; one 15 s connector retry) | under |
| 1 | ~60 min (~10 ingest) | ~16 min (ingest 4.5 min; 4 eval runs ~1.2–1.4 min each, serial) | well under |
| 2 | ~35 min | ~6 min | under |
| 3 | ~30 min | ~5 min | under |
| 4 | ~45 min (~5 re-embed) | ~11 min (family loads 3.5 min total) | under |

No lab exceeded 1.5× budget; all ran well under. Stated budgets are
generous for a scripted run and reasonable for a learner reading the
"Why" blocks.

## Checkpoint table

### Lab 0: Setup

| Checkpoint | Verdict | Observed |
| --- | --- | --- |
| 0.1 version/distribution | PASS | 3.5.0 / opensearch, valid TLS |
| 0.2 corpus verified | PASS | `OK: 1072 files verified. 8955 chunks, 300 golden queries, 10000 tickets.` |
| Step 3 model group | PASS | `{"status":"CREATED"}` |
| Step 4 register+deploy | PASS | task COMPLETED in ~30 s; `model_state: DEPLOYED` on first check |
| 0.3 predict determinism | PASS | `dimensions: 384`, first 3 values `[-0.048449516, -0.019668244, 0.025217716]`, exact match |
| Step 6 connector create | PASS w/ retry | first attempt HTTP 500 `"Fetching master key timed out"` (cluster-side, not provider); succeeded on retry after 15 s |
| Step 6 remote model deploy | PASS w/ note | model registered instantly with `model_id`; state stayed `PARTIALLY_DEPLOYED` after two `_deploy` calls, but predicts worked flawlessly (Step 4's partial-deploy box covers the situation, though it appears under the embedding model, not Step 6) |
| 0.4 `connected` | PASS | output was exactly `connected` |

### Lab 1: Simple RAG & Hybrid Search

| Checkpoint | Verdict | Observed |
| --- | --- | --- |
| 1.1 chunk anatomy | PASS | `chunk_id: DOC-00001#0.0`, `acl: public`, `parent_text` present |
| Steps 2–4 pipeline/index/alias/fusion | PASS | all `{"acknowledged":true}` |
| Step 5 ingest | PASS | `Done. 8955 chunks indexed into support-docs-v1 in 4.5 min.` One `bulk rejection at 800: backing off 10s, halving batch`, the documented backpressure behavior, recovered automatically |
| 1.2 counts | PASS | count 8955; missing-embedding count 0 |
| 1.3 error-code query | PASS | filtered rank 1 `ERR-2209: Connector handshake failed` at **2.919**, next 2.219 (lab: ~2.9 vs ~2.2); unfiltered top-3 dominated by api-reference + ticket chunks, as narrated |
| 1.4 vague symptom | PASS | BM25 top-3 off-topic (`Troubleshooting pagination`, `Troubleshooting API authentication`, `How pagination works`); neural rank 1 `Troubleshooting dashboard rendering` |
| 1.5 hybrid two ways | PASS | both pipelines return connector-handshake/Snowflake tickets; RRF scores 0.033–0.016, weighted 1.00–0.28, orderings differ, scales wildly differ, exactly as taught |
| 1.6 acl pre-filter | PASS | all 5 hits `acl: public` |
| 1.7 ablation table | PASS w/ note | see eval table; 11 of 12 cells within ~0.02, one (rrf MRR) at 0.021; ordering contract holds |
| 1.8 tuned fusion | PASS | tuned hit rate 0.613 vs rrf 0.540 (+0.073 ≥ 0.05) |

**Eval metrics as measured** (k=5, kb_only, 300 queries, runs serial):

| mode | hit_rate@5 | precision@5 | MRR | reference | max delta |
| --- | --- | --- | --- | --- | --- |
| bm25 | 0.497 | 0.116 | 0.308 | 0.513 / 0.123 / 0.319 | 0.016 |
| neural | 0.630 | 0.146 | 0.336 | 0.633 / 0.147 / 0.339 | 0.003 |
| hybrid-rrf | 0.540 | 0.133 | 0.302 | 0.550 / 0.139 / 0.323 | **0.021** |
| tuned (0.2/0.8) | 0.613 | 0.143 | 0.338 | 0.610 / 0.141 / 0.337 | 0.003 |

Ordering contract: neural (0.630) > hybrid-rrf (0.540) > bm25 (0.497)
on hit rate (holds. Tuned beats rrf by 0.073 ≥ 0.05) holds. The one
cell outside ~0.02 (rrf MRR, 0.302 vs 0.323, delta 0.021) is within
the tie/HNSW variance the lab itself explains; this run's ingest also
took one backpressure batch-halving mid-run, consistent with the
lab's footnote about segment-layout drift.

### Lab 2: RAG with Memory

| Checkpoint | Verdict | Observed |
| --- | --- | --- |
| 2.1 turn-two junk | PASS | top-3: `Troubleshooting mobile layouts`, `Incremental Refresh overview`, `How email delivery works`, nothing about ERR-2209 |
| 2.2 tenant isolation | PASS | hits: 2 then hits: 0 |
| 2.3 skip logic | PASS | `True / False / True / False` exactly |
| 2.4 LLM rewrite (LLM path) | PASS | see LLM outputs section; rewritten retrieval top-3 all connector-handshake ERR-2209 content (scores 1.84–1.82) vs Step 1 junk |
| 2.5 HyDE (LLM path) | PASS | vague query top-3 = 3 tickets ("Dashboard takes forever to load" variants); HyDE-passage top-3 = 3 product-docs (`Troubleshooting dashboard rendering`, `How dashboard rendering works`, `Troubleshooting dashboard rendering`) |
| 2.6 _msearch decomposition | PASS | two sub-responses matching the lab's printed block title-for-title |
| 2.7 ISM policy | PASS | created and read back `_id: support-conversation-retention` |
| Step 9 Memory API (optional) | PASS | memory created, message added, thread read back |

### Lab 3: Corrective RAG

| Checkpoint | Verdict | Observed |
| --- | --- | --- |
| 3.1 impossible answer | PASS | known-issue text shows `Affected versions: 4.8, 4.9` / `Fixed in: 5.0` / workaround "available in 5.0 and later" |
| 3.2 score shapes | PASS | healthy `2.92 2.22 2.22 2.22 2.18 2.18 2.18 2.18` (lab: 2.92 2.21…2.18, 0.01 drift on tail); sick `1.75 1.75 1.75 1.75 1.73 1.73 1.73 1.73` (lab: 1.74/1.73). Shapes identical: clear leader vs flat huddle |
| 3.3 _explain | PASS | `_explanation` tree with `sum of:`, per-term idf/tf details |
| 3.4 correction loop, 3 outcomes | PASS | 4.8 run: `version fit` FAILs on all 3 attempts (incl. the bonus `granularity: section truncated…` on attempt 1), ends `LOW CONFIDENCE: retry budget (2) spent.` in exactly 3 attempts; 5.1 and ERR-2288/4.9 runs both `CONFIDENT after 0 correction(s)` with zero FAIL lines |
| 3.5 explain-back | PASS | demonstrated by 3.4: grader consumed lesson-1.3 metadata |
| 3.5b LLM grader (LLM path) | PASS | see LLM outputs section, `"pass": false` with a version reason, first try |
| 3.6 traces agg | PASS | `connectors` bucket, avg_faithfulness 0.91, avg_retries 2.0 |

### Lab 4: Agentic RAG

| Checkpoint | Verdict | Observed |
| --- | --- | --- |
| Step 1 four indexes | PASS | four acknowledged (MAPCOMMON/EMB fragments pasted as written) |
| Step 2 family loads | PASS | `Done.` ×4 in 3.5 min total; issues loaded instantly with no pipeline |
| 4.1 aliases + counts | PASS | `support-docs → support-docs-v2`; counts **5068 / 3816 / 15 / 56** exactly |
| 4.2 per-index strategy | PASS | `ERR-2288: Schema discovery timed out` rank 1 on issues; tickets weighted search returns "Schema list never finishes loading…" variants |
| 4.3 ReAct trace | PASS | iter 1 observed ERR-2288 facts (information_schema >120 s, scope-schemas workaround, affected 4.8–5.0, fixed 5.1); iter 2 returned `How to configure schema discovery | Common errors` ×2 |
| 4.4 _msearch meta-tool | PASS | three sub-responses from three indexes: known issue / docs pages / ERR-2209 tickets. Note: docs sub-search titles were `Connector Credential Rotation settings reference` ×2 rather than TLS-specific pages (see findings) |
| 4.5 route cache | PASS | paraphrase hit score **1.9316** (~1.93), route `howto_path`; unrelated query `{}` at min_score 1.7, raw score **1.2011** (~1.20) |
| 4.6 answer cache | PASS | 5.1 hit (1.9438, cached answer returned); 4.8 `{}`; `_delete_by_query` deleted exactly **1** |
| 4.7 guardrails recitation | PASS | four ceilings (iterations ≤5, tokens, wall clock, cost) and "stop, answer from evidence, flag confidence, escalate", internally consistent and matches Lab 3's retry-budget behavior as claimed |
| 4.8 end-to-end RAG (LLM path) | PASS | see LLM outputs section, 5.1 answer prescribes TLS 1.3 with chunk citations; 4.8 answer flags the 5.0 gate as not applicable |

## LLM-path outputs (verbatim, judged behaviorally)

All via the Cohere connector (`command-a-03-2025`, temperature 0). No
predict call needed a retry; the only transient error of the entire
run was the connector-creation 500 in Lab 0. Calls were spaced ≥5 s
apart.

**Checkpoint 0.4**, prompt "Reply with exactly the word: connected":

```
connected
```

**Lab 2 Step 5 rewrite** (must restore error code + connector topic + version):

```
How to enable TLS 1.3 in connector advanced settings for version 4.9 to resolve ERR-2209 TLS handshake failure?
```

Verdict: PASS, ERR-2209, TLS/connector topic, and 4.9 all restored
(identical to the lab's sample, notably). Retrieval with it returned
connector-handshake ERR-2209 content at ranks 1–3, night-and-day
against Checkpoint 2.1's `Troubleshooting mobile layouts` junk.

**Lab 2 Step 6 HyDE paragraph** (must read like documentation and retrieve docs, not tickets):

```
Recent updates to the platform's data processing engine may have introduced temporary
inconsistencies in dashboard rendering. Users experiencing unusual behavior are advised
to clear their browser cache and reload the dashboard, as this often resolves issues
related to outdated or conflicting data and UI elements. If problems persist, please
contact support with specific details about the affected dashboards for further
investigation.
```

Verdict: PASS, documentation voice; retrieval flipped from 3 tickets
to 3 dashboard-rendering product-docs pages (top score 1.779).

**Lab 3 Step 4b grader** (verdict must be pass:false with a version reason):

```
{"pass": false, "reason": "The customer is on version 4.8, and the workaround requires version 5.0 or later."}
```

Verdict: PASS, correct verdict, version-grounded reason, valid
one-line JSON, no prompt tightening needed.

**Lab 4 Step 9, customer on 5.1** (must prescribe TLS 1.3 with chunk-ID citations):

```
packed 8 parent sections: ['DOC-00404#0.0', 'DOC-00639#0.0', 'DOC-00498#2.0', 'DOC-00028#2.0',
'DOC-00263#2.0', 'DOC-00298#3.0', 'DOC-00445#2.0', 'DOC-00210#2.0']

To fix **ERR-2209**, you need to enable **TLS 1.3** in the connector advanced settings. This
resolution is available in **version 5.0 and later** [DOC-00298#3.0, DOC-00445#2.0,
DOC-00210#2.0]. Since the customer is on **version 5.1**, this solution applies to their version.

**Steps to resolve ERR-2209:**
1. Navigate to the connector settings.
2. Access the advanced settings.
3. Enable **TLS 1.3**.

This issue was fixed in version 5.0, and versions 4.8 and 4.9 were affected [DOC-00298#3.0,
DOC-00445#2.0, DOC-00210#2.0].
```

Verdict: PASS, prescriptive, chunk-ID citations on every claim.

**Lab 4 Step 9, customer on 4.8** (must flag the 5.0 gate rather than present the fix as actionable):

```
The error **ERR-2209** occurs because the **TLS negotiation failed** due to the warehouse
requiring **TLS 1.3**, which is not supported in your current version (4.8) [DOC-00298#3.0,
DOC-00445#2.0, DOC-00204#2.0].

The resolution for this issue is to **enable TLS 1.3 in the connector advanced settings**,
but this feature is only available in **version 5.0 and later** [DOC-00298#3.0, DOC-00445#2.0,
DOC-00204#2.0]. Since you are on version 4.8, this fix is not applicable.

To resolve ERR-2209 on your current version, you would need to **upgrade to version 5.0 or
later** [DOC-00298#3.0, DOC-00445#2.0, DOC-00204#2.0].
```

Verdict: PASS, explicitly states "this fix is not applicable" on 4.8;
the course's central failure case is beaten.

## Issues found

No blocks-learner or misleads-learner issues on this run. Findings, in
descending severity:

1. **friction, Lab 0 Step 6: `"Fetching master key timed out"` on
   first connector create.** HTTP 500 `m_l_exception` from the
   cluster on the very first `/_plugins/_ml/connectors/_create` after
   a fresh wipe (ML master key lazily initialized). Cleared on one
   retry ~15 s later. The lab's transient-error caveat lists provider
   errors (429/503/NO_VALID_RESPONSE_GENERATED) but not this
   cluster-side one, and it happens at the exact step a nervous
   learner is pasting their first credential. Repro: wiped cluster,
   run Step 6 connector create as the first-ever ML-connector call.
   Suggested lab-text fix: add one sentence to Step 6, e.g. "If the
   very first connector call returns `Fetching master key timed out`,
   the cluster is initializing its ML encryption key; re-run the same
   command."

2. **friction (minor), Lab 0 Step 6: remote LLM model can sit in
   `PARTIALLY_DEPLOYED`.** Observed after both the initial `_deploy`
   and one re-run; Checkpoint 0.4 nevertheless passed instantly and
   every later predict worked. Step 4 documents this state for the
   embedding model; Step 6 says nothing, and a learner who checks
   `model_state` (as Step 4 taught them to) will see a state the step
   never mentions. Suggested fix: one line after the Step 6 deploy:
   "Remote models may show PARTIALLY_DEPLOYED on shared clusters;
   Checkpoint 0.4 is the real test."

3. **cosmetic (numeric drift, within the labs' own stated variance) , 
   Lab 1 Checkpoint 1.7:** hybrid-rrf MRR measured 0.302 vs reference
   0.323, delta 0.021, a hair over the "~0.02 per cell" phrasing; the
   other 11 cells were within 0.016 and both ordering contracts held
   comfortably. The lab's explanation (BM25 ties + HNSW variance,
   plus this run's mid-ingest batch-halving) covers it. Suggested
   fix: none required; optionally phrase as "~0.02–0.03 per cell; the
   orderings are the contract."

4. **cosmetic, Lab 3 Step 2 exact score lists:** measured
   `2.92 2.22 2.22 2.22 2.18…` and `1.75 1.75 1.75 1.75 1.73…` vs
   printed `2.92 2.21…` and `1.74…1.73` (±0.01 on tail values). The
   shape contract (leader-and-drop vs flat huddle) is fully intact.
   Same BM25 corpus-statistics drift Lab 1 explains. Suggested fix:
   none, or add "(tail values may drift by ±0.01)".

5. **cosmetic, Lab 3 Step 4 narrative vs printout:** the lab
   narrates attempt 0 as "score shape passes," while the script
   prints `score shape: flat (top=2.92)`. The gate does pass (flat
   only alarms when top < 2.0, per the script's comment), but a
   learner cross-reading the word "flat" against "passes" may
   hesitate. Suggested fix: narrate as "score shape passes the gate
   (flat but high, many similar candidates, not a miss)".

6. **cosmetic, Lab 4 Step 5 expected docs titles:** the docs
   sub-search returned `Connector Credential Rotation settings
   reference` ×2 rather than pages whose titles telegraph the TLS
   fix. The lab's prose ("connector docs pages") is loose enough to
   cover this, and Checkpoint 4.4 (three sub-responses, three
   indexes) is unambiguous and passed. Suggested fix: none, or soften
   the parenthetical to "connector-related docs pages."

7. **note, corpus verifier on macOS:** prints
   `note: 1 extra file(s) not in manifest (ignored): ['.DS_Store']`
   before the OK line. Harmless, correctly ignored, and consistent
   with Checkpoint 0.2's "ends with OK" wording.

Zero points required a decision the labs did not cover, beyond the two
Lab 0 Step 6 frictions above (retry the 500; accept
PARTIALLY_DEPLOYED). Every ID substitution (model_group_id, task_id,
MODEL_ID, connector_id, LLM_ID) was unambiguous from the lab text.

## State left on the cluster (no cleanup, per instructions)

Indices: `support-docs-v1` (8955), `support-docs-v2` (5068),
`support-tickets-v1` (3816), `support-issues-v1` (15),
`support-api-v1` (56), `support-conversations` (2), `support-traces`
(1), `support-route-cache` (1), `support-answer-cache` (0 after
invalidation). Aliases: `support-docs`→v2, `support-tickets`,
`support-issues`, `support-api`. Ingest pipelines: `support-embed`,
`support-cache-embed`. Search pipelines: `support-hybrid-rrf`,
`support-hybrid-weighted`, `support-hybrid-tuned`,
`support-tickets-weighted`. ISM policy:
`support-conversation-retention`. ML: model group
`support-embedding-models`, embedding model (all-MiniLM-L6-v2,
DEPLOYED), connector `support-llm-cohere`, remote model `support-llm`
(PARTIALLY_DEPLOYED, functional), one ML memory ("CONV-LAB2 native").
Cluster health: green throughout and at the end.
