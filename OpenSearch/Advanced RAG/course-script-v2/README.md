# Course Script v2 (Chapters 2 through Conclusion)

Updated 2026-07-10 to match what three full validation runs on the live
demo cluster actually show on screen. Each file keeps the lesson /
voice-over / visuals structure of the Word drafts and ends with a
change log against the current draft, so review is a diff-read, not a
re-read.

- `chapter-2-rag-with-memory.md` (2.1, 2.2, 2.3)
- `chapter-3-corrective-rag.md` (3.1, 3.2, 3.3; contains the one
  substantive rewrite, in 3.2)
- `chapter-4-agentic-rag.md` (4.1, 4.2, 4.3)
- `conclusion.md` (5.1, 5.2)
- `CHAPTER-1-RECORDING-NOTES.md` (the complete change list for the
  chapter already at the agency: five one-word VO fixes, the rest is
  demo-capture guidance)

Demo callouts in the visuals columns reference Example Corp Data Kit
lab steps (`example-corp-kit/labs/`), so every on-screen capture can be
reproduced by running the lab.

## Introduction (0.1 / 0.2): not rewritten, two flags

The intro was outside the requested scope but has two items to settle
before it records:

1. Lesson 0.2 says "One system, five chapters" and the layer-cake
   visual labels the conclusion "Ch5 Decision framework," while the
   course has four chapters plus a conclusion (whose lessons are
   numbered 5.1/5.2). Pick one term and use it in both VO and visuals.
2. Lesson 0.2 says "Everything runs on OpenSearch 3.6 on the
   Instaclustr Managed Platform." Validation ran on 3.5.0 (3.6 not yet
   offered); either record after a 3.6 validation pass or soften the
   version claim. Same decision as note 11 in the Chapter 1 file.
   Also worth one added sentence somewhere in 0.2 or the labs intro:
   the companion corpus is demo scale (1,000 docs pages, 10,000
   tickets) so ingest is polite on a trial cluster; the narrated 8,000
   pages and 200k tickets describe Example Corp's fictional full
   estate.
