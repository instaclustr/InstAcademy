# The RAG runner

Run the full RAG loop end to end: OpenSearch does the embeddings, vector
storage, and hybrid retrieval, and a language model of your choosing
writes the answer from the evidence the cluster returns. No credit card
on any path, and no LLM connector inside the cluster.

Generation is pluggable through `LLM_BACKEND`:

| Backend | What it is | Cost |
|---|---|---|
| `groq` (default) | `openai/gpt-oss-120b`, hosted | free tier, API key, no payment details |
| `gemini` | Google AI Studio, not part of the course path | free tier, but only 20 requests per day |
| `ollama` | a model on your own machine | nothing, and no signup |

If the key for a cloud backend is missing, the runner says so and falls
back to Ollama rather than refusing to start.

**Which to use.** The course uses `groq` so the chapters behave the same
on every machine. A model small enough to run comfortably on an average
laptop does not hold the five-block prompt reliably: handed a question
the evidence only half covers, it invents the missing half more readily
and declines less often than a larger model does. Use `ollama` if you
would rather not sign up for anything, or as the escape hatch when a
free tier runs out mid-chapter, and expect looser wording and less
consistent citations. Chapter 2 Step 5 has an optional step that uses
`ollama` deliberately, to show that difference side by side.

Runs on macOS, Linux, and Windows. Standard library only, nothing to
install. Validated on a 3.5.0 cluster with Groq. LLM wording
varies run to run; retrieval is deterministic. See the caveat below.

## What runs where

| Piece | Technology | Where it runs |
|---|---|---|
| Embeddings | all-MiniLM-L6-v2 via ML Commons | OpenSearch cluster |
| Vector store, kNN, BM25, hybrid fusion | OpenSearch | OpenSearch cluster |
| Orchestration (embed, retrieve, prompt, generate) | stdlib Python, no pip | your laptop |
| Generation | Groq, Gemini, or Ollama | hosted, or your laptop |

The generation model only writes text. It never embeds, so a plain
Ollama server having embeddings turned off does not matter. Everything
heavy stays on the cluster, which is why this runs on a low-spec laptop.

## Prerequisites

0. **Chapter 1 finished**, so the `support-advrag-kb` index exists and an
   embedding model is deployed. These forms query what Chapter 1 built;
   they do not build anything themselves.
1. A generation backend. Either a free Groq API key from
   [console.groq.com/keys](https://console.groq.com/keys), or Ollama
   running locally with a small chat model (`ollama pull llama3.2:3b`,
   about 2 GB).
2. Python 3 (standard library only, nothing to install). On macOS and
   Linux the command is usually `python3`; on Windows it is `python`.
3. Network access to the OpenSearch load balancer.

## One-time setup: create your .env file

Configuration lives in a `.env` file in this folder, so you fill it in
once and never retype it. Copy the template, then edit the copy.

macOS / Linux:

    cd rag-runner
    cp .env.example .env

Windows (PowerShell or Command Prompt):

    cd rag-runner
    copy .env.example .env

Then open `.env` in any editor and set your values:

    OS_URL=https://<your-load-balancer-host>:9200
    OS_USER=<user>
    OS_PW=<password>
    LLM_BACKEND=groq
    GROQ_API_KEY=<your-groq-key>

`.env` is git-ignored and must not be committed or shared: it holds your
cluster password. If you would rather not use a file, you can still set
these as shell environment variables and they take precedence over `.env`.

## Steps

Run each from inside this folder. Use `python3` on macOS/Linux or
`python` on Windows.

    python3 05_rag_chat_server.py
      Starts a browser chat UI. Open http://localhost:8787 and ask
      questions. Ask sends a question; Clear empties the chat. Each
      answer shows the sources it was grounded on. Bound to
      127.0.0.1, so only your machine can reach it. Stop with Ctrl-C.

    python3 06_rag_chat_memory.py
      The Chapter 4 capstone: the same loop as 05, plus conversation
      memory through the ML Commons Memory API. On startup it creates a
      memory and prints its memory_id; each turn is stored, the history
      is read back to rewrite follow-ups into standalone queries, and
      recent turns ride into the prompt alongside the evidence. Open
      http://localhost:8788 (a different port from 05, so both can run
      at once). Needs the Chapter 3 hybrid search pipeline. Delete the
      memory it prints when you are done, as Chapter 4 cleanup shows.

    python3 teardown.py
      Removes every support-* asset this lab created (index, pipelines,
      model, model group) so the shared cluster is left clean.

## Why a chat app cannot do this on its own

A chat window, whether that is the Groq console, the Ollama desktop app,
or `ollama run`, talks straight to the model. None of them have a step
that retrieves from OpenSearch, so none of them can ground an answer in
the Example Corp corpus. Something has to retrieve first and put the
evidence into the prompt. That is what `05_rag_chat_server.py` does. If you want a fuller browser front-end, Open WebUI can call
OpenSearch through a custom pipeline the same way these scripts do, but
it needs its own install.

## Results-may-vary caveat

Retrieval (which documents come back, and in what order) is
deterministic for a given corpus and model, so the sources and
rankings reproduce. The generated wording comes from the language model
and will differ slightly each run and between models. What should stay
constant is the behavior: the answer is grounded in the retrieved
evidence, it cites sources, and it declines when the answer is not in
the corpus.

## Files

- `.env.example` copy to `.env` and fill in (config template)
- `.gitignore` keeps `.env` and run artifacts out of git
- `osc.py` shared OpenSearch + LLM client, dispatches on `LLM_BACKEND` (loads `.env`)
- `05_rag_chat_server.py` browser chat UI (Ask + Clear), single-turn
- `06_rag_chat_memory.py` browser chat UI with conversation memory (Chapter 4)
- `teardown.py` remove all support-* assets
