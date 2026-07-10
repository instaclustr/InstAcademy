# CLAUDE.md: Course Kit Validation

You are validating the hands-on portion of the "Advanced RAG with
OpenSearch" learning path against a live cluster. Two jobs, in order:

1. **Infrastructure validation:** execute `TEST_SPEC.md` Part 1
   (phases P0-P9). Does every script, query, and pipeline in the kit
   actually work on this cluster?
2. **Lab pedagogy validation:** execute Part 2. Walk each lab in
   `labs/` exactly as a learner would, top to bottom, and verify every
   Checkpoint. Does the lab teach what it claims, and do the stated
   expectations match reality?

## Repo map

```
CLAUDE.md              this file
TEST_SPEC.md           the full test spec (Part 1 infra, Part 2 labs)
corpus/                example-corp-corpus-v2.1.0.tar.gz (canonical batch)
scripts/               stdlib-only learner scripts the labs invoke
kit/
  code-samples/        per-lesson request bodies (lesson-X-Y.md)
  generators/          maintainer corpus generators
labs/
  lab-0-setup.md       environment + model deploy
  lab-1-simple-rag.md  Chapter 1: ingest, retrieval strategies, eval + tuning
  lab-2-memory.md      Chapter 2: conversations, rewriting, HyDE, _msearch, ISM
  lab-3-corrective.md  Chapter 3: score shapes, correction loop, traces
  lab-4-agentic.md     Chapter 4: index split, ReAct, caches, guardrails
```

## Hard rules (repeated from the spec because they matter)

- Credentials come only from the `OS_URL` env var. Never print, log, or
  write them anywhere, including the report.
- Touch only `support-*` prefixed resources (plus the ML model group
  `support-embedding-models` and models registered into it). Never
  modify cluster settings; if one is needed, stop and report it.
- Use the pre-built corpus in `corpus/`; do not regenerate (the labs
  depend on the canonical batch).
- Labs must be run IN ORDER (0, 1, 2, 3, 4); later labs depend on
  earlier state. Do not clean up between labs.
- Cleanup only if `CLEANUP=true` is set.
- Be polite to the shared cluster: serial requests, modest batches,
  check `_cluster/health` before and after heavy phases.

## Output

Write `TEST_REPORT.md` in the repo root, structured per the spec's
Deliverable section, including the lab-by-lab checkpoint table from
Part 2 and any drift between lab-stated expected values and observed
values (the labs print exact numbers; exactness is the contract).
