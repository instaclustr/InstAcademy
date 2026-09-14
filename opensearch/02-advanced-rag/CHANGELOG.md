← **Back to:** [Course index](README.md) · [How to run labs](HANDS-ON-GUIDE.md) · [Cluster setup](CLUSTER-SETUP.md)

# Changelog

All notable changes to this course are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the course uses [semantic versioning](https://semver.org/) adapted for learning material:

- **Major** (2.0.0): a restructure that changes the chapter or lesson lineup, so anyone mid-course would need to restart.
- **Minor** (1.1.0): steps added, removed, or renumbered inside a chapter, or a new OpenSearch version validated.
- **Patch** (1.0.1): corrections, clearer wording, updated screenshots, no change to what you run.

## [1.1.0] - 2026-09-11

Chapter 2 is now **9 steps**: the request that re-runs Step 3's three conflicting sections through the five blocks was an unnumbered section and is now **Step 5** ("The question Steps 2 and 3 could not answer"). Every later step in the chapter shifted up by one — the chat form is now Step 9 — and all references across the course were updated to match (41 steps total). If you are mid-course from an earlier version, only the numbering changed; no step was added to or removed from what you actually run.

## [1.0.1] - 2026-09-09

Windows validated. Every terminal step was re-executed on Windows 11, in PowerShell 5.1 and 7 and in Git Bash, against the same OpenSearch 3.5.0 cluster, and all cluster-side Expected blocks reproduced.

- Added a **[Windows users](HANDS-ON-GUIDE.md#windows-users)** section to the lab guide and a **Windows (PowerShell)** note at every terminal step, so the whole course runs from PowerShell with nothing extra installed: `python` in place of `python3`, generation through an `Invoke-RestMethod` helper (`Ask-Groq`) instead of `curl`, and `Set-Content`/`Add-Content` instead of `echo >` for the runner's files.
- Fixed `teardown.py`, which targeted pre-release asset names and would not have removed this course's index or pipelines; fixed the matching stale index default in `05_rag_chat_server.py`.
- Full findings are in the Windows section of the [validation report](example-corp-kit/TEST_REPORT.md).
- Aligned chapter formatting with the Vector Storage and Search course: sentence-cased chapter titles, `🚀 Next chapter` and `🏁 Course wrap-up` headings, and the request-your-badge link in the course wrap-up.

## [1.0] - 2026-08-12

Initial release. The course is complete: four chapters of hands-on workshops, 40 steps, validated end to end against a live OpenSearch 3.5.0 cluster with generation running on Groq's free tier.

## Compatibility

| Course version | Validated on | Cluster | Generation |
|---|---|---|---|
| 1.0 | OpenSearch **3.5.0** (Lucene 10.3.2) | NetApp Instaclustr managed, AI Search Plugin, 3 data nodes (t4g.medium) | Groq `openai/gpt-oss-120b`, free tier |

Every chapter needs the **AI Search Plugin** (ML Commons and k-NN). Chapter 4's Memory API steps need OpenSearch **3.5 or later**. Chapters 2, 3, and 4 additionally need a free **Groq API key** and **Python 3** on your own machine, not on the cluster. The terminal steps are validated from **macOS** and from **Windows 11** in PowerShell, with nothing extra installed; see the [Windows users](HANDS-ON-GUIDE.md#windows-users) section of the lab guide.

**On BM25 scores across versions.** The keyword scores in Chapter 3 come from this 3.5.0 run. BM25 uses collection-wide term statistics, so its absolute scores can move between OpenSearch and Lucene versions even on an identical corpus. Treat the ordering and the size of the gap between hits as the signal, not the third decimal. The vector scores, which are cosine similarities, reproduce far more tightly.

## Reproducibility

The full step-by-step validation results, including what did not reproduce and every defect
found, are in [`example-corp-kit/TEST_REPORT.md`](example-corp-kit/TEST_REPORT.md).

Every **Expected** block that comes from the cluster is the response from the validated run. Retrieval order reproduces reliably; absolute scores can move by a couple of hundredths. Every **Expected** block that comes from the language model also comes from a live run, pinned to `temperature: 0`, but wording still drifts between runs. Those steps are judged by behavior, not by wording.

| Datapoint | Value |
|---|---|
| Documents in the knowledge base | 1,079 |
| Chunks indexed | 5,139 (of 8,955 in the corpus file; support tickets are excluded on purpose) |
| Golden set | 300 queries |
| Chapter 1 baseline (neural, k=5) | hit rate 0.653 · precision 0.151 · MRR 0.359 |
| Chapter 3 keyword (bm25, k=5) | hit rate 0.603 · precision 0.143 · MRR 0.377 |
| Chapter 3 hybrid (RRF, k=5) | hit rate 0.670 · precision 0.167 · MRR 0.381 |

Those three rows come from one validated run and move between runs, because approximate vector search and RRF tie-breaking both depend on an internal document order a fresh load can change. Across validated runs each figure has stayed within about a hundredth of the value above (re-running the idempotent loader shifts BM25's collection statistics slightly, which is enough to move the second decimal). What reproduces exactly is the ordering: hybrid wins hit rate and precision, and MRR is a three-way near-tie.

---

← **Back to:** [Course index](README.md) · [How to run labs](HANDS-ON-GUIDE.md) · [Cluster setup](CLUSTER-SETUP.md)
