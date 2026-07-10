# Chapter 1: updates needed (VO already at the agency)

Good news first: **the Chapter 1 voice-over needs almost nothing.**
Everything the hands-on validation surfaced lands in the visuals and
demo captures, not the narration. Here is the full list, ordered by
whether it touches the recording.

## VO text fixes (send to the agency before they record these lines)

1. **Lesson 1.1, "Keyword, vector, sparse" segment:** the draft reads
   "This is where dense vector search **earns excels**." Two verbs
   collided in editing; it should be one of them, e.g. "This is where
   dense vector search excels." A narrator reading verbatim will trip
   here.
2. **Lesson 1.2, reranking segment:** "It's also **expensive an
   expensive** operation." Duplicated word; should read "It's also an
   expensive operation."
3. **Lesson 1.3, parsing segment:** "strip the noise from the
   **boilerplatesm**" is a typo for "boilerplates." Spoken aloud it
   will probably come out right anyway, but fix the script copy.
4. **Lesson 1.3, chunking segment:** "So Which strategy should be
   used..." has a mid-sentence capital; cosmetic in text, irrelevant to
   VO.
5. **Lesson 1.3, ingestion segment:** "re-running a job should never
   **duplicates** anything" should be "duplicate."

That is the entire VO list. None of these change meaning; if the
narrator has already recorded them and read them smoothly, nothing
needs re-recording except item 1, which is unreadable as written.

## Visuals / demo-capture guidance (no VO impact)

6. **Lesson 1.1's on-screen symptom query.** The VO says "my dashboard
   takes forever to load" and claims no docs page uses those words. In
   the validated corpus, real *tickets* use exactly that phrasing, so a
   live unfiltered demo of that query makes BM25 look great and
   undercuts the point. Keep the VO as narration, but capture the demo
   using the validated lab query, "charts spin forever and never
   appear," restricted to product docs: BM25 returns pagination and API
   authentication junk; neural returns "Troubleshooting dashboard
   rendering" at rank 1. That is the on-screen proof of the exact claim
   the VO makes.
7. **Lesson 1.1, error code demo.** Unfiltered, ERR-2209 surfaces
   mostly ticket chunks at similar scores. For the "clear leading
   score" frame the VO implies, capture the knowledge-base-filtered
   query from Lab 1 Step 6 (known issue at 2.92 vs 2.21 below).
8. **Lesson 1.2 / 1.3, the ablation table.** If any slide shows eval
   numbers, use the validated reference table (bm25 0.513 / neural
   0.633 / hybrid-rrf 0.550 / tuned 0.610 hit rate at 5) with a
   "within a couple hundredths, run to run" footnote. Two full
   validation runs proved exact third-decimal reproduction is not
   achievable (BM25 score ties and HNSW construction vary with ingest
   history); the ordering always reproduces. Also know the headline:
   on THIS golden set, neural beats unweighted hybrid, and the tuning
   step is what makes hybrid competitive. The Chapter 1 VO never claims
   otherwise, so no narration change; just do not add a slide that says
   "hybrid wins the table."
9. **Lesson 1.3 golden set count.** Slides should say 300 golden
   queries (the corpus ships 300; the VO's "two hundred labeled
   queries" line is advice about the customer's own data and can
   stand).
10. **Lesson 1.4 demo captures.** All ingest/connector demos should be
    captured from Lab 0 / Lab 1 runs: the model group + register +
    deploy flow, the fail-loudly zero-missing-embeddings check, and the
    alias flip (Lab 4 Step 2 performs the 1.4 alias flip live if you
    want real footage).

## Version framing (decide once, applies to all chapters)

11. The course narrates OpenSearch 3.6 features (Lucene BBQ in 1.1;
    agentic memory, token tracking, V2 chat agent in chapters 2 and 4).
    Everything hands-on validated on 3.5.0; the 3.6-only features are
    narration-only and unvalidated. If recording finishes before a 3.6
    cluster is available for a validation pass, consider softening
    "3.6 adds..." to "the newest OpenSearch releases add..." so the
    audio does not need re-cutting if a claim shifts. The Chapter 1
    instance is one sentence in lesson 1.1.

## Stale header items in the Chapter 1 doc (production hygiene)

12. The doc header still has: empty Learn Path Title, "{To be written}"
    course summary, "TBC" resource links, and a "Target Length: 90
    minutes" line (the current full-course runtime math is 82.5
    minutes). None of it is VO, but the agency may copy header fields
    into deliverables.
