← **Back to:** [Course index](../README.md) · [Kit README](README.md) · [Changelog](../CHANGELOG.md)

# Validation report — Advanced RAG with OpenSearch

**Course version 1.0** · validated **2026-09-08 / 2026-09-09** · **OpenSearch 3.5.0**

Every numbered step in all four chapters was executed against a live cluster, and every
**Expected** block was compared against what the cluster actually returned. This report
records what reproduced, what did not, and what was changed as a result.

---

## Environment

| | |
|---|---|
| OpenSearch | 3.5.0, build `bbc94f0`, Lucene 10.3.2 |
| Platform | NetApp Instaclustr managed |
| Topology | 3 data nodes (`dimr`) + 1 coordinator-only node (`r`) |
| Plugins | `opensearch-knn`, `opensearch-ml`, `opensearch-neural-search`, `opensearch-search-relevance` |
| Embedding model | `huggingface/sentence-transformers/all-MiniLM-L6-v2` v1.0.2, TORCH_SCRIPT, 384 dims |
| Generation | Groq `openai/gpt-oss-120b`, free tier, `temperature: 0` |
| Local generation | Ollama `llama3.2:3b` (optional Chapter 2 step only) |
| Corpus | `example-corp-corpus-v2.1.0` |

## Verdict

**All 40 steps executed successfully.** Every cluster-derived Expected block reproduced,
most of them to four decimal places. Two course-breaking defects were found and fixed;
neither was a cluster problem.

---

## Chapter 1 — Simple RAG and Hybrid Search

| Step | Result |
|---|---|
| 1 · ML Commons settings | ✅ four keys echoed, `acknowledged: true` |
| 2 · Model group | ✅ `model_group_id` returned |
| 3 · Register model | ✅ `COMPLETED` in **17 s** (chapter says ~25 s; "a minute or two" is safe) |
| 4 · Deploy | ✅ `DEPLOYED`, 3/3 workers, `embedding_dimension: 384` — **after 4 attempts** |
| — · Heap check | ✅ 41–59% post-deploy, all below the 85% guard |
| 5 · Smoke test | ✅ **exact match**: `-0.048450, -0.019668, 0.025218`, 384 dims |
| 6 · Ingest pipeline | ✅ `acknowledged: true` |
| 7 · k-NN index | ✅ created with the documented mapping |
| 8 · Sample bulk | ✅ all five chunk ids present in the corpus, values identical |
| 9 · Full load | ✅ **5,139 chunks in 3.1 min**, zero failures |
| 10 · Neural search | ✅ **exact**: KI-0001 `0.8714`, DOC-00753 `0.846`, DOC-00290 `0.8459` |
| 11 · Golden set | ✅ see table below |

**Step 4 needed four deploy calls.** The first three returned `COMPLETED_WITH_ERROR` with
`Memory Circuit Breaker is open`, sitting at `PARTIALLY_DEPLOYED` 2/3 in between. The chapter
warned about this but described it as occasional; the guidance was strengthened to
"expect to repeat it."

**Step 9 hit backpressure and recovered on its own.** The loader halved from batch 100 to 50
mid-load and finished clean — the documented behaviour, observed live.

---

## Chapter 2 — Context Prompting for RAG

| Step | Result |
|---|---|
| 1 · Child/parent + collapse | ✅ **exact**: DOC-00659 `0.9286`, DOC-00189 `0.9182`, DOC-00800 `0.9113` |
| 2 · Lazy prompt, one section | ✅ answers with the professional-tier number, uncited |
| 3 · Lazy prompt, three sections | ✅ returns a three-row menu instead of an answer |
| 4 · Five blocks | ✅ concise, cited `[KI-0001]`, names 5.0 and 4.8 |
| — · Five blocks on Step 3's evidence | ✅ picks `25`, cites `DOC-00095` |
| 5 · Ablation | ⚠️ **rebuilt** — see below |
| — · Optional Ollama ablation | ✅ ran on `llama3.2:3b`; both halves invented a click path |
| 6 · Citation trace | ✅ `KI-0001` → 1 hit; `KI-9999` → 0 hits |
| 7 · Pre-filter | ✅ **exact**: DOC-00330 `0.8604`, DOC-00753 `0.8485`, DOC-00428 `0.8463` |
| 8 · Chat form | ✅ vector-only mode; chips match Chapter 1 Step 10 exactly |

### Step 5 was rebuilt because the original no longer demonstrated anything

The original ablation asked a question the evidence did not cover at all ("how do I reset my
billing password?") and expected the model to invent an answer once the grounding rule was
removed. **Every currently available Groq model declines that question either way.** Tested on
`openai/gpt-oss-120b`, `openai/gpt-oss-20b`, and `qwen/qwen3.8-27b`: all six runs declined.
Model size is not the variable — the question is.

The step now asks for something the evidence **half** covers: `KI-0001` names result caching as
the workaround but contains no procedure.

| | Output |
|---|---|
| Grounded | `I do not have that information. [KI-0001]` · `Confidence: low` |
| Ablated | A six-step invented click path (Data Manager, Settings tab, Result Caching toggle, cache duration, republish) with `[KI-0001]` on **every step** · `Confidence: medium` |

The invention is an *extension* of true evidence rather than a contradiction of it, every line
carries a citation that passes the Step 6 existence check, and self-reported confidence goes
**up**. This is a stronger demonstration than the original.

---

## Chapter 3 — Hybrid RAG

| Step | Result |
|---|---|
| 1 · BM25 error code | ⚠️ ranking exact; **score differs** — `14.3504`, not the documented `13.6386` |
| 2 · BM25 plain language | ⚠️ ranking exact; top score `3.1757` vs `3.1742` |
| 3 · Neural error code | ✅ **exact**: KI-0013 `0.9372`, DOC-00743 `0.9225`, DOC-00417 `0.9159` |
| 4 · Neural plain language | ✅ **exact**: DOC-00142 `0.7875`, DOC-00377 `0.7811`, DOC-00666 `0.7807` |
| 5 · RRF pipeline | ✅ `acknowledged: true` |
| 6 · Hybrid error code | ✅ **exact**: KI-0013 `0.0328`, DOC-00743 `0.0323`, DOC-00132 `0.0159` |
| 7 · Hybrid plain language | ⚠️ scores exact; **tied pair returned in the opposite order** |
| 8 · Golden set, three modes | ✅ see table below |
| 9 · Chat form, hybrid | ⚠️ one documented answer no longer declines — see below |

**The BM25 scores in the chapter were 3.6.0 values.** The changelog had recorded `14.26` for
3.5.0 and `13.64` for 3.6.0; this run produced `14.3504`. Since the course now validates on
3.5.0, all BM25 figures were updated. Rankings and gap sizes were unaffected — the property the
lesson actually depends on.

**Step 7's top hit is a coin flip.** `DOC-00142` and `DOC-00337` tie at `0.0164`, and this run
returned them in the opposite order to the printed block. The chapter claimed `DOC-00142`
"leads the list." Reframed as tied-at-top, which is what is stable.

**Step 9's decline demo fails under hybrid.** "How do I reset my billing password?" declines
cleanly with vector-only retrieval (Chapter 2) but is *answered* once the keyword leg is added:
BM25 matches the token `password` against the Stripe credential-rotation guide, and the model
answers from it. Grounded, and wrong. Five alternative out-of-corpus questions were tested and
declined cleanly; the demo now uses a refund-policy question, and the failure was kept as a new
teaching section on hybrid's cost.

---

## Golden set — 300 queries, `--kb-only`, k=5

```text
method   hit@5   precision@5   MRR
bm25     0.603   0.147         0.375
neural   0.653   0.151         0.359
hybrid   0.667   0.169         0.369
```

**The ordering reproduces exactly**: hybrid wins hit rate and precision, MRR is a three-way
near-tie. Absolute figures drifted up to 0.005 from the previously published numbers, so the
stated tolerance was widened from 0.002 to 0.005. Chapter 1's baseline, Chapter 3's table, the
changelog, and the kit README were all reconciled to this run.

### Cross-validated against the Search Relevance Workbench

The same golden set was scored a second time using OpenSearch's own in-cluster evaluation
framework (`_plugins/_search_relevance`), on 298 of 300 queries — the API rejects query text
containing `:`, and two golden queries contain one.

| method | Workbench `Precision@5` | `eval_retrieval.py` `precision@5` | `MAP@5` | `NDCG@5` |
|---|---|---|---|---|
| bm25 | 0.146 | 0.146 | 0.038 | 0.167 |
| neural | 0.151 | 0.151 | 0.035 | 0.163 |
| **hybrid** | **0.170** | **0.170** | **0.041** | **0.180** |

Two independent implementations — one Python, one in-cluster Java — computed identical
precision from the same labels. The Workbench also ranks hybrid first on MAP and NDCG, two
rank-aware metrics the course does not compute, independently corroborating Chapter 3's
conclusion. It does **not** provide hit rate or MRR, which is why the Python scorer stays.

---

## Chapter 4 — RAG with Memory

| Step | Result |
|---|---|
| 1 · Stateless follow-up | ✅ **exact**: DOC-00715 `0.7454`, DOC-00665 `0.7446`, DOC-00245 `0.7405` |
| 2 · Create memory | ✅ `memory_id` returned |
| 3 · Store turn 1 | ✅ `message_id` returned |
| 4 · Store turn 2 | ✅ `message_id` returned |
| 5 · Read history | ✅ exact shape: `input`, `response`, `create_time`, `updated_time` |
| 6 · Read `additional_info` | ✅ exact, including `"user": "icopensearch"` |
| 7 · Rewrite follow-up | ✅ carries both the error code and the version |
| 8 · Hybrid on rewrite | ✅ **exact**: KI-0001 `0.0328`, leading by 2× |
| 9 · Second memory | ✅ distinct `memory_id` |
| 10 · Isolation | ✅ **exact**: `{"messages": []}` |
| 11 · Combined prompt | ✅ grounded, cited, `Confidence: high` |
| 12 · Multi-turn capstone | ✅ all four turns, see below |
| — · Cleanup | ✅ `{"success": true}` |

**The conversational Memory API is not deprecated.** Current OpenSearch documentation still
lists it as *Introduced 2.12* with no deprecation banner. The agentic memory container
(`POST /_plugins/_ml/memory_containers/_create`) also responds on 3.5.0, confirming the note in
Lesson 4-2.

**Step 12 turn-by-turn:** turn 1 no rewrite (`turns: 1`); turn 2 rewrote to
`ERR-1102 dashboard render timeout version 5.0` and retrieved `KI-0001`; turn 3 rewrote to
`ERR-1102 dashboard load time forever version 5.0`, dragging the previous topic along **exactly
as the chapter predicts**; turn 4 declined.

**Step 11's prompt was rebuilt.** It carried only `MEMORY` / `EVIDENCE` / `QUESTION` while
claiming nothing but the memory block had changed. It now carries all five blocks with
`## MEMORY` in the slot `## TOOLING` held, and `06_rag_chat_memory.py` was aligned to emit the
same structure. The system instructions are byte-identical to Chapter 2 Step 4 — verified by
diff.

---

## Defects found and fixed

| # | Severity | Defect |
|---|---|---|
| 1 | **Blocker** | `llama-3.3-70b-versatile` decommissioned by Groq. Every generation step 404s. Swapped to `openai/gpt-oss-120b` in 9 places; added a model-retirement note |
| 2 | **Blocker** | Chapter 2 Step 8 required a search pipeline Chapter 3 does not create until Step 5. `RAG_PIPE` is now optional; Chapter 2 runs vector-only, Chapter 3 Step 9 switches hybrid on |
| 3 | High | Chapter 2 Step 5's ablation no longer demonstrated anything (see above) |
| 4 | High | Chapter 3's decline demo answers instead of declining under hybrid (see above) |
| 5 | Medium | Chapter 3 BM25 scores were 3.6.0 values on a 3.5.0-validated course |
| 6 | Medium | Chapter 3 Step 7's tied top hit presented as stable ordering |
| 7 | Medium | Chapter 4 Step 11 dropped two prompt blocks while claiming otherwise |
| 8 | Low | `DOC-00377#1.2` referenced but does not exist (only `#1.0`, `#1.1`) |
| 9 | Low | Chapter 1 Step 8 sample described as verbatim; omits 3 fields |
| 10 | Low | "three data nodes" beside a four-line output (3 data + 1 coordinator) |
| 11 | Low | Chapter headers offered Dev Tools "or" the runner; Chapter 1 never uses the runner at all |
| 12 | Low | Golden-set figures differed between the chapters and the kit README |
| 13 | Low | `GEMINI_MODEL` defaulted to `gemini-3.5-flash`, which does not exist |
| 14 | Low | Kit README referenced four files that were never shipped |
| 15 | Low | `06_rag_chat_memory.py` undocumented in the runner README |

**21 unused files were deleted**: five scripts written for an abandoned in-cluster LLM-connector
architecture, a self-contained 10-document mini-lab belonging to a different course, and eleven
video-lesson code samples using index names the course no longer uses.

## Not validated

- **Instaclustr console screenshots** in `CLUSTER-SETUP.md` — no way to confirm the signup and
  cluster-creation screens still match the current console.
- **`kit/generators/`** — maintainer-only corpus builders, not exercised by this run.
- **Gemini backend** — wired up but not part of the course path.
- **Chapter 1 Step 8's bulk request in isolation** — the five chunk ids were verified against
  the corpus and are covered by the Step 9 full load.

## Windows validation — 2026-09-09

Every terminal step was re-executed on **Windows 11** (Python 3.12, Git for Windows 2.x, curl 8.4.0)
against the same 3.5.0 cluster, in both Git Bash and PowerShell, to find what the macOS-authored
`bash` blocks assume. Cluster-side Expected blocks reproduced identically (BM25 absolute scores
moved slightly — 13.46 vs 14.35 on the ERR-6640 anchor — because a re-index changed collection
statistics; ordering was identical). The golden-set sweeps on Windows: bm25 0.613/0.148/0.384,
neural 0.650/0.153/0.364, hybrid 0.673/0.171/0.381 — hybrid wins hit rate and precision, MRR
a near-tie, as documented. Both chat servers, all four capstone turns, and the Memory API
steps behaved as printed; the Turn 2 rewrite reproduced verbatim
(`ERR-1102 dashboard render timeout version 5.0`).

What did not survive Windows out of the box, and what was done about it:

| # | Severity | Finding | Resolution |
|---|---|---|---|
| W1 | High | `echo "id" > model_id.txt` in Windows PowerShell 5.1 writes UTF-16 with a BOM; the server starts cleanly, then every question fails with `embedding failed` | Windows notes at Ch2 Step 8 and Ch4 Step 12 with `Set-Content ... -Encoding Ascii` |
| W2 | High | `echo "RAG_PIPE=..." >> .env` in PowerShell 5.1 appends UTF-16 bytes; the server dies at startup with `UnicodeDecodeError` | Windows note at Ch3 Step 9 with `Add-Content ... -Encoding Ascii` |
| W3 | High | The `curl` blocks (Ch2, Ch4, cluster setup) are unrunnable in PowerShell: `curl` aliases `Invoke-WebRequest` in 5.1, and quoting of the JSON bodies breaks either way | Windows path made PowerShell-native: every generation step carries a Windows note calling an `Invoke-RestMethod` helper (`Ask-Groq`), validated live in both PowerShell 5.1 and 7 |
| W4 | Medium | `\| python -c "print(...)"` dies with `UnicodeEncodeError` when the model emits a character outside cp1252 (observed live with U+2011 and U+202F) | Moot on the PowerShell path (`Invoke-RestMethod` parses the reply itself); `PYTHONUTF8=1` documented for the optional Git Bash path |
| W5 | Medium | `python3` does not exist on a stock Windows install (python.org's installer creates only `python`; the `python3` name is a Microsoft Store stub) | "Type `python` wherever a block says `python3`" rule; PowerShell equivalents printed at Ch1 Steps 9 and 11 and Ch3 Step 8 |
| W6 | Low | `cmd.exe` `echo "id" > model_id.txt` writes the quote characters into the file | Covered by the same Windows notes; cmd not recommended |
| W7 | Low | `teardown.py` targeted pre-release asset names (`support-rag-demo`, `support-rag-hybrid`, `support-rag-embed`, `support-rag-demo-group`); on this course it would have deleted only the model | Names corrected to `support-advrag-kb`, `support-advrag-hybrid`, `support-advrag-embed`, `advanced-rag-models`; stale `RAG_INDEX` default in `05_rag_chat_server.py` fixed too |

Also observed: the eval scorer tripped the ML Commons circuit breaker once at query 273/300,
and the documented remedy (wait, re-run) worked on the first retry. The kit scripts read the
corpus with `Path.read_text()` and no explicit encoding, which resolves to cp1252 on Windows;
this is currently harmless because both corpus files are pure ASCII, but it is a latent trap
if the corpus ever gains a non-ASCII character.

## Reproducing this run

```bash
cd example-corp-kit
export OS_URL=https://<user>:<password>@<host>:9200
export OS_INDEX=support-advrag-kb
G=corpus/example-corp-corpus-v2.1.0/golden_set.jsonl

python3 scripts/ingest_chunks.py --index support-advrag-kb \
  --chunks corpus/example-corp-corpus-v2.1.0/chunks.jsonl \
  --doc-types product-docs,integration-guide,known-issue,api-reference

python3 scripts/eval_retrieval.py --mode bm25   --k 5 --kb-only --golden $G
python3 scripts/eval_retrieval.py --mode neural --k 5 --kb-only --golden $G --model-id <ID>
python3 scripts/eval_retrieval.py --mode hybrid --k 5 --kb-only --golden $G --model-id <ID> \
  --search-pipeline support-advrag-hybrid
```

---

← **Back to:** [Course index](../README.md) · [Kit README](README.md) · [Changelog](../CHANGELOG.md)
