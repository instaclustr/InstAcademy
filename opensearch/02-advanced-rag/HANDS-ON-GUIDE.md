← **Previous:** [Cluster setup](CLUSTER-SETUP.md) · [Course index](README.md) · **Next:** [Chapter 1](chapters/01-simple-rag-and-hybrid-search/README.md) →

# How to run the labs

This page is the entry point for the hands-on part of the course. Read it once, then work through the chapters in order. Each chapter is a single workshop page at `chapters/Chapter N/README.md` that walks through every step of that chapter, and you run those steps against your own OpenSearch cluster.

**Before you start:** you need a running cluster, its connection details, and a free Groq API key for the generation steps. If you don't have those yet, go to [cluster setup](CLUSTER-SETUP.md) first; it takes about 10 minutes.

---

## How a chapter is laid out

Every chapter follows the same shape, so once you've done one, you know how to read them all.

| Element | What it is |
|---|---|
| **Lesson N-M** | A section of the workshop, teaching one concept and the steps that build it |
| **Step N** | One thing you do, numbered across the whole chapter. |
| **Request** | The exact code to run, ready to copy: a REST call for Dev Tools, or a command for your terminal |
| **Expected** | The response from the validated run, and what the interesting parts of it mean |
| **Save** | A value (a model id, a memory id) that a later step needs |

Steps build on each other, so work through them in order.

## The two places a step runs

### Dev Tools (everything on the cluster)

Dev Tools is the console built into OpenSearch Dashboards, where most of this course runs. To get there:

1. Open your **Dashboards URL** in a browser. It's on the **Connection Info** tab of your cluster in the Instaclustr console, and it looks like this (note the port, **5601**, not 9200):

   ```
   https://opensearch-dashboards.<your-cluster-id>.cnodes.io:5601
   ```

2. Log in with the same username (`icopensearch`) and password you use for the cluster (found on the 'connection info' page).
3. Open the menu at the top left, scroll to **Management**, and choose **Dev Tools**. Or jump straight there:

   ```
   https://opensearch-dashboards.<your-cluster-id>.cnodes.io:5601/app/dev_tools#/console
   ```

You'll see a split screen: type requests on the left, responses appear on the right. Paste a **Request** from the chapter page, press **Ctrl+Enter**, and compare what comes back to the **Expected** block.

### Your terminal (loading data, scoring, and generation)

Some steps run from your own terminal: the bulk loader and the golden-set scorer in Chapters 1 and 3, and every step where a language model writes an answer. Those Requests are shell commands rather than REST calls, and they are marked as `bash` blocks.

Every `cd` in those blocks starts from the repo folder — the one that contains `example-corp-kit`. If you reuse a terminal from an earlier step, it may still be sitting in a subfolder like `rag-runner`, and the `cd` will fail with "no such directory"; hop back up first (`cd ..` from `example-corp-kit`, `cd ../..` from `rag-runner`). The steps where this commonly happens carry a reminder in the block itself.

Two different folders in the kit, with two different configuration styles, and it's worth getting this right once:

| Where | What it is | How it authenticates |
|---|---|---|
| `example-corp-kit/scripts/` | the bulk loader and the golden-set scorer | one env var, `OS_URL`, with credentials inline: `https://user:password@host:9200` |
| `example-corp-kit/rag-runner/` | the browser chat forms | a `.env` file in that folder with **separate** `OS_URL`, `OS_USER`, and `OS_PW`, your `LLM_BACKEND` and its API key, plus a `model_id.txt` file |

You set the runner folder up once, at [Chapter 2 Step 9](chapters/02-context-prompting-for-rag/README.md#step-9-launch-the-chat-form-and-ask-a-grounded-question), which walks through it when you first need it: copy `.env.example` to `.env`, fill in your cluster details and Groq key, and write your `ML_MODEL_ID` into `model_id.txt`.


[!Note]
> **A note if you watched the videos first.** The videos describe generation running on the learner's own machine. The lab gives you both the option to do a local model or a hosted model instead since many computers may not have the resources to run a model locally. The architecture is identical either way: OpenSearch does the retrieval, the prompt is the same prompt, and the model only writes the answer from the evidence it is handed.
>
> Models small enough to run comfortably on an average laptop do not hold the five-block prompt reliably: handed a question the evidence only half covers, they invent the missing half more readily and decline less often than a larger model does. Using a free tier keeps the Expected blocks consistent and keeps your hardware out of it.
>


### Windows users

The `bash` blocks in this course are written for macOS and Linux. On Windows the whole course runs from **PowerShell** and is validated end to end on Windows 11 with Python 3.12. Every terminal step carries a **Windows (PowerShell)** note with the exact lines to run instead of the printed block. 3 Things to know:

**1. Type `python` wherever a block says `python3`.** The python.org installer does not create a `python3` command on Windows. The other translations are just as mechanical: `$env:OS_URL = "..."` instead of `export OS_URL=...`.

**2. The generation steps call Groq through this helper.** The printed blocks use `curl`, which does not work with PowerShell's quoting. Paste this once per session, and each generation step's Windows note becomes a single `Ask-Groq` call:

```powershell
function Ask-Groq($body) {
  (Invoke-RestMethod https://api.groq.com/openai/v1/chat/completions -Method Post -ContentType "application/json" -Headers @{ Authorization = "Bearer $env:GROQ_API_KEY" } -Body $body).choices[0].message.content
}
```

**3. Never create or append to the runner's files with `echo` and `>`.** Windows PowerShell 5.1 writes UTF-16 there: a `model_id.txt` written that way makes every chat question fail with `embedding failed`, and a `.env` appended that way stops the server at startup with a `UnicodeDecodeError`. The Windows notes at Chapter 2 Step 9 and Chapter 3 Step 9 use `Set-Content` and `Add-Content` instead.


## Things worth knowing before you start

**All of the data is fictitious.** Example Corp is not a real company, and every document, ticket, known issue, error code, and version number in the knowledge base was generated for this course. The real product names you will see in the integration guides, like Stripe and PostgreSQL, are only there to make the corpus read like real documentation. The [course index](README.md#a-note-on-the-data) has the full note.

**Values you carry forward.** A few steps produce ids that later steps need: `model_group_id`, `task_id`, `model_id`, and in Chapter 4 the `memory_id` values. Each one is flagged with **Save** where it appears. Keep them in a scratch file. The one you'll use constantly is `ML_MODEL_ID`, from Chapter 1 Step 3.

## Course order

| Chapter | What you build |
|---|---|
| [Chapter 1](chapters/01-simple-rag-and-hybrid-search/README.md) | Deploy an embedding model, build the ingest pipeline and index, load 5,139 chunks, retrieve, and score the baseline |
| [Chapter 2](chapters/02-context-prompting-for-rag/README.md) | Pack parent sections as evidence, then wrap them in a structured, cited, version-aware prompt |
| [Chapter 3](chapters/03-hybrid-rag/README.md) | Run keyword, vector, and fused search on the same questions, then score all three on the golden set |
| [Chapter 4](chapters/04-rag-with-memory/README.md) | Store conversations in the Memory API, rewrite follow-ups, join user context to the knowledge base, and chat with the whole system |

---

### Ready to start some hands-on fun??
**Cluster running, connection details saved, Groq key in hand?** Start with [Chapter 1](chapters/01-simple-rag-and-hybrid-search/README.md)!

---

← **Previous:** [Cluster setup](CLUSTER-SETUP.md) · [Course index](README.md) · **Next:** [Chapter 1](chapters/01-simple-rag-and-hybrid-search/README.md) →
