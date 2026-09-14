# Example Corp Data Kit

Everything the hands-on side of the "Advanced RAG with OpenSearch"
learning path needs that is not the lab text itself: the canonical
Example Corp demo corpus, the stdlib-only scripts the labs invoke, the
runner that generates answers, and the maintainer tooling that builds
the corpus.

**The labs themselves live next door**, at
[`../chapters/`](../chapters/), one page per chapter. Start there, not
here. This kit is what those pages point at.

> **All of the data in this kit is fictitious.** Example Corp is not a
> real company, and every document, ticket, known issue, error code, and
> version number was generated for the course. Real product names in the
> integration guides, such as Stripe, Slack, and PostgreSQL, appear only
> to make the corpus read like real documentation. Nothing here comes
> from, describes, or is affiliated with or endorsed by those companies.

## Layout

```
README.md            this file
TEST_REPORT.md       results of the last end-to-end validation run
corpus/
  example-corp-corpus-v2.1.0/   the canonical corpus batch
scripts/             stdlib-only Python the labs invoke (no pip installs)
  ingest_chunks.py       Chapter 1 Step 9 bulk loader (batches, backpressure, resumable)
  eval_retrieval.py      Chapter 1 Step 11 and Chapter 3 Step 8 scorer (hit@k, precision@k, MRR)
  oscommon.py            shared OpenSearch client (reads OS_URL with inline credentials)
rag-runner/            the browser chat forms
  05_rag_chat_server.py  Chapter 2 Step 8 and Chapter 3 Step 9
  06_rag_chat_memory.py  Chapter 4 Step 12
  osc.py                 shared OpenSearch + LLM client (reads .env)
  teardown.py            removes every support-* asset (not referenced by a chapter)
kit/
  generators/            maintainer-only corpus generators (requires `requests`)
```

## Two configuration styles, and they differ

This trips people up, so it is worth stating plainly:

| Folder | Reads | Notes |
|---|---|---|
| `scripts/` | `OS_URL` only, with credentials **inline**: `https://user:password@host:9200` | one env var, nothing else |
| `rag-runner/` | a `.env` file with **separate** `OS_URL`, `OS_USER`, `OS_PW` | also needs a `model_id.txt` holding your deployed `model_id`, or the chat servers exit at startup |

## Design rules

- **Copy-paste first.** Every cluster interaction a learner performs is
  pasted from a lab page, with what it does and what to expect stated
  at each step. No hidden setup.
- **No credit card, ever.** The embedding model (`all-MiniLM-L6-v2`, 384
  dims) runs inside the cluster, so retrieval never leaves it. Generation
  calls a hosted model through the runner's own client, not through an
  OpenSearch LLM connector, so nothing in the cluster holds a generation
  credential. The default is Groq (`openai/gpt-oss-120b`), whose free
  tier asks for an API key and no payment details; the runner also
  accepts `gemini`, and `ollama` for a model on the learner's own
  machine. No billing information is required on any path.
- **No pip installs.** Every script in `scripts/` and
  `rag-runner/` is standard library only.
- **One prefix.** Every cluster resource the course creates is named
  `support-*`, so cleanup is one wildcard and collisions are
  impossible.
- **Same data, same model, same numbers.** Learners verify the corpus
  against a sha256 manifest and never regenerate locally. Embedding
  vectors are identical for every learner. Retrieval order reproduces;
  absolute scores can move by a couple of hundredths.

## What is in the corpus (canonical batch v2.1.0)

| Asset | Count | In the knowledge base? |
| --- | --- | --- |
| Product docs pages | 1,000 (4,750 chunks) | yes |
| Integration guides | 50 (318 chunks) | yes |
| API reference | 14 pages (56 chunks) | yes |
| Known issues DB | 15 (15 chunks) | yes, one record per chunk, no parent |
| Ticket history | 10,000 (3,816 chunks) | **no**, tickets are the source of the golden queries |
| Chunks, total in the file | 8,955 | 5,139 of them load into the knowledge base |
| Golden query set | 300 labeled queries | the answer key for Chapter 1 Step 11 and Chapter 3 Step 8 |

Chapter 1 Step 9 passes
`--doc-types product-docs,integration-guide,known-issue,api-reference`,
which is what makes the loaded count come out at exactly 5,139. Tickets
stay out on purpose: they are where the golden questions came from, so
retrieving them back would be circular.

Counts are demo scale on purpose. Full-scale ingest on a shared cluster
would be impolite and nothing pedagogical changes. Everything is
deterministic under `--seed 42` and internally consistent across all
five assets, which is what makes the golden set labels free.

## Cluster prerequisites

OpenSearch 3.5 or later, with k-NN, ML Commons, and neural-search. On the **NetApp Instaclustr Managed
Platform** the **AI Search Plugin** add-on covers all three. No
dedicated ML node is required, but
`plugins.ml_commons.only_run_on_ml_node` must be `false`, which
Chapter 1 Step 1 sets.

Validated end to end on OpenSearch 3.5.0, Instaclustr managed, three
data nodes with no dedicated ML nodes. Every step of all four chapters
was executed against a live cluster; see [TEST_REPORT.md](TEST_REPORT.md)
for what reproduced and what changed as a result.

## Validated numbers

Reproduced live against the full 5,139-chunk knowledge base:

```text
method   hit@5   precision@5   MRR      (300 golden queries, --kb-only, k=5)
bm25     0.603   0.147         0.375
neural   0.653   0.151         0.359
hybrid   0.667   0.169         0.369
```

Hybrid wins coverage and precision; ranking is a three-way near-tie.
That table is the argument Chapter 3 is built on, and it is the same
table printed in Chapter 3 Step 8. Each figure moves by up to about
0.005 between runs; the ordering is what reproduces.

## Maintainer: rebuilding the corpus

Learners never do this. Any generator change is a new corpus version:

```bash
cd kit/generators
python build_release.py --version <NEW_VERSION>
```

That builds, checksums, and verifies reproducibility. Re-validate the
labs before distributing a new batch, then update the version string
everywhere it appears in the chapter pages and in `scripts/`.
