# Course Kit Validation Spec

## PART 1: Infrastructure validation (the kit works)

Objective: validate the Example Corp Data Kit end to end against a live
OpenSearch cluster and produce a TEST_REPORT.md. Every demo shown on
camera and every lab command must actually run.

## Ground rules

1. **Credentials.** The cluster URL with credentials is provided as the
   `OS_URL` env var, format `https://user:pass@host:9200`. Never print,
   log, echo, or commit this value.
2. **Blast radius.** Only create, modify, or delete `support-*`
   prefixed resources (indexes, aliases, ingest pipelines, search
   pipelines, ISM policies) plus the `support-embedding-models` ML
   model group and models registered into it. Never change
   cluster-level settings; stop and report if one is needed.
3. **Scale.** Use the canonical corpus as-is (demo sizes). Never run
   full-scale generation against a shared cluster.
4. **Politeness.** Serial requests, modest batches. Check
   `_cluster/health` before and after heavy phases; if status leaves
   green, pause and record it.
5. **Idempotence.** Every phase must be safely re-runnable; the loaders
   auto-resume and index by stable `_id`.
6. **Stop on ambiguity.** If the cluster lacks a plugin or gates a
   feature by version, record it and continue with what remains
   possible.
7. **TLS.** Instaclustr certs are valid; keep verification on.

## P0: Preflight

```
GET /                       -> version.number, distribution
GET /_cluster/health        -> status (accept green or yellow)
GET /_cat/plugins?v         -> confirm: opensearch-knn, opensearch-ml,
                               opensearch-neural-search, opensearch-index-management
GET /_cat/nodes?v&h=name,node.roles,heap.max  -> at least one ml-role node
```

Feature gates by version: hybrid + normalization-processor (2.10+),
score-ranker-processor RRF (2.19+), Memory APIs (2.12+), neural query
`filter` param (2.13+), agentic memory / token tracking / Lucene BBQ
(3.6, note-only below 3.6).

## P1: Corpus (local only)

```bash
cd corpus && tar xzf example-corp-corpus-v2.1.0.tar.gz && cd ..
python3 scripts/verify_corpus.py --corpus corpus/example-corp-corpus-v2.1.0
```

Pass = `OK: 1072 files verified. 8955 chunks, 300 golden queries,
10000 tickets.` Cross-consistency spot check: ERR-2209 appears in a
docs page, a guide, known_issues.jsonl, at least one ticket, and at
least one golden query's label chain.

## P2-P8: Run the labs (they ARE the infra test)

The labs are the canonical command sequence; there is no separate
script path anymore. Execute `labs/lab-0-setup.md` through
`labs/lab-4-agentic.md` in order, literally, as Part 2 describes below.
Key hard assertions along the way:

- **Lab 0:** model predict returns a 384-dim vector whose first three
  values are `-0.048449516, -0.019668244, 0.025217716` (determinism
  contract). LLM path (Step 6): connector + remote model deploy
  succeeds and Checkpoint 0.4 prints `connected`. LLM outputs
  everywhere are judged behaviorally (per the Lab 0 variance caveat),
  never verbatim; transient provider errors
  (429/503/NO_VALID_RESPONSE_GENERATED) are retried, not failed.
- **Lab 2 LLM steps:** the model's rewrite restores the error code,
  connector topic, and version; its HyDE paragraph reads like docs and
  retrieves dashboard rendering docs (not tickets) at the top.
- **Lab 3 Step 4b:** the LLM grader returns `"pass": false` with a
  version-related reason.
- **Lab 4 Step 9:** the 5.1 answer prescribes TLS 1.3 with chunk-ID
  citations; the 4.8 answer flags the 5.0 requirement instead of
  presenting the fix as actionable.
- **Lab 1:** `support-docs` count = 8,955; zero docs missing
  `embedding`; eval table within ~0.02 per cell of the reference
  (kb_only): bm25 0.513/0.123/0.319, neural 0.633/0.147/0.339,
  hybrid-rrf 0.550/0.139/0.323, tuned weighted (0.2/0.8)
  0.610/0.141/0.337. Exactness is NOT expected (BM25 ties + HNSW vary
  with ingest history); the hard contract is the ordering
  neural > hybrid-rrf > bm25 on hit rate and tuned > rrf by >= 0.05.
- **Lab 2:** cross-tenant read returns 0; skip logic (word-count
  threshold 4) prints True/False/True/False; `_msearch` returns two
  topical sub-responses; ISM policy and Memory API calls succeed
  (Memory API needs 2.12+).
- **Lab 3:** healthy shape `2.92 2.21 ...` vs sick flat `1.74 ...`;
  4.8/ERR-2209 run shows `version fit` FAILs and ends LOW CONFIDENCE in
  <= 3 attempts; 5.1/ERR-2209 and 4.9/ERR-2288 end CONFIDENT with 0
  corrections; traces agg returns avg_faithfulness 0.91.
- **Lab 4:** four aliases resolve (docs alias flipped to v2); counts
  5,068 / 3,816 / 15 / 56; ERR-2288 rank 1 on support-issues;
  route-cache paraphrase scores ~1.93 (hit at min_score 1.7) and the
  unrelated query ~1.20 (miss); answer-cache hits for 5.1, misses for
  4.8; `_delete_by_query` invalidation deletes exactly 1.

Known cluster quirk (observed on OpenSearch 3.5.0): `_reindex` between
these indexes intermittently reports `batches: 0` and copies nothing
without error. The labs therefore use `scripts/split_chunks.py` (bulk +
pipeline) instead of `_reindex`. If validating on a newer version,
retest `_reindex` and note the result.

## P9: Cleanup (only with operator confirmation, `CLEANUP=true`)

1. List and print everything matching `support-*` (indices, aliases,
   ingest pipelines, search pipelines, ISM policies).
2. Delete indices `support-*`; ingest pipelines `support-embed`,
   `support-cache-embed`; search pipelines `support-hybrid-rrf`,
   `support-hybrid-weighted`, `support-hybrid-tuned`,
   `support-tickets-weighted`; ISM policy
   `support-conversation-retention`; any ML memory created in Lab 2.
3. Undeploy and delete the registered model + model group ONLY if this
   run registered them.

## Deliverable: TEST_REPORT.md

- Date, cluster version/distribution, plugins, node shape, feature
  gates hit
- Per-lab checkpoint table: checkpoint / PASS-FAIL-AMBIGUOUS / observed
  value or output excerpt
- Per-lab wall time vs the lab's stated budget (>1.5x over is a
  finding)
- Eval metric table as measured
- Issues found, each with severity (blocks-learner / misleads-learner /
  friction / cosmetic), reproduction, and suggested lab-text fix

---

## PART 2: Lab pedagogy validation (the labs teach correctly)

Run every lab in `labs/`, in order (0, 1, 2, 3, 4), exactly as written,
as if you were a learner following it for the first time. Test three
things at once:

1. **Executability:** every command runs as written, from the kit root
   directory, with only the env vars the labs establish (`OS_URL`,
   `MODEL_ID`, `OS_INDEX`, and Lab 4's `MAPCOMMON`/`EMB` fragments).
2. **Expectation accuracy:** every "Expected result" and Checkpoint
   matches what actually happens. The labs promise exact numbers;
   exactness is the contract.
3. **Pedagogical soundness:** at each "Why" / "How it should feel" /
   "explain-it-back" block, judge whether the explanation is (a)
   technically accurate, (b) sufficient for a learner who has only
   watched the lessons up to that point, and (c) actually demonstrated
   by the step it accompanies. Flag any place where the lab asserts
   something the learner's screen does not show.

Reset nothing between labs; the dependency chain is itself under test.
Note every point where you had to make a decision the lab did not
cover; each one is a finding, because a human learner stops there.

### Severity rubric for lab findings

- **blocks-learner:** a command fails, a checkpoint is factually wrong,
  or a dependency on prior state is broken. A learner cannot continue.
- **misleads-learner:** the step runs but the output contradicts or
  fails to demonstrate the "Why" text.
- **friction:** works, but requires an unstated decision.
- **cosmetic:** typos, formatting, ordering nits.
