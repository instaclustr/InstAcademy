# Course Review Notes: Advanced RAG with OpenSearch

Findings from the full build-and-validate pass (2026-07-09). Organized
by what needs your decision vs. what I already fixed vs. editorial
issues in the two Word documents. Work through this top to bottom when
you're back.

---

## 1. Needs your decision

### 1.1 The demo cluster is OpenSearch 3.5.0, the course targets 3.6+
Every lab step validated cleanly on 3.5.0, so nothing in the hands-on
path is blocked. But four things the course *narrates* are 3.6 features
that cannot be validated on this cluster:

- Lucene BBQ (Better Binary Quantization, "32x compression"), lesson 1.1
- Agentic memory in the agent framework, lessons 2.2, 4.1
- Per-interaction token usage reporting, lessons 4.1, 4.3
- V2 chat agent, lesson 4.1

**Recommendation:** re-run the final verification on a 3.6 cluster when
Instaclustr offers it, before recording. The labs themselves say
"3.1+ (course targets 3.6+)" so they will not mislead anyone on 3.5.

### 1.2 Old SupportAI-branded artifacts: DELETED (2026-07-10, per Brian)
The old kit folder (`supportai-course/`), both zips
(`supportai-course.zip`, `supportai-data-kit.zip`), and the stashed
previous lab drafts (`example-corp-kit/labs-old/`) were deleted at
Brian's direction after the new kit passed validation. The
`Advanced RAG/` folder now contains only: the two Word docs, the
validated `example-corp-kit/`, the v2 scripts in `course-script-v2/`,
and this file.

### 1.3 Search pipeline names
Course script text never names the search pipelines; old kit used
unprefixed `hybrid-rrf` / `hybrid-weighted`. I renamed everything to a
`support-` prefix (`support-hybrid-rrf`, `support-hybrid-weighted`,
`support-tickets-weighted`) so every cluster resource the course
creates shares one prefix, cheaper to clean up, impossible to collide
with another tenant's pipelines. If the recorded videos already show
the old names, say so and I'll revert.

### 1.4 LLM path: RESOLVED into a dual-path design (2026-07-10)
Per your direction, the labs now have two paths. **Primary:** a real
LLM (learner brings a free key, no card) connected through an ML
Commons connector in Lab 0 Step 6; both supported providers' endpoints
are pre-trusted on Instaclustr clusters. Live-LLM steps: Lab 2 rewrite
+ HyDE, Lab 3 LLM grader (4b), Lab 4 end-to-end RAG answer with
citations (Step 9). All carry the variance caveat and behavioral
checkpoints. **Secondary:** every LLM step has a "No-LLM alternative"
box with the validated by-hand text, so the course stays fully
runnable with zero keys.

**Validation outcome:** **Cohere is the validated provider** (trial
key, `command-a-03-2025`). The full LLM path ran live end to end, and
every sample output in the labs is a real recorded output: the rewrite
restored code+topic+version, the HyDE paragraph retrieved
`Troubleshooting dashboard rendering` at rank 1, the grader returned
`pass: false` on version fit, and the capstone RAG answers behaved
correctly for both customers (the 4.8 answer honestly says
upgrade-or-escalate, no workaround). Trial-tier quirk: occasional
transient `NO_VALID_RESPONSE_GENERATED` errors that clear on retry;
the Lab 0 caveat covers this. **Gemini is written but unvalidated:**
your key authenticated, but Google's free tier now has zero quota on
older models for new projects, and the one eligible model
(`gemini-flash-latest`) was capacity-throttled (503) for the entire
validation window. Decide whether to keep Gemini in Lab 0 as the
second option (my lean: yes, learners in other regions/time windows
will get through, and dual-provider is insurance) or go Cohere-only
until Gemini validates.

### 1.5 Corpus scale vs. course narration
The narration says 8,000 docs pages / 200k tickets; the canonical demo
corpus is 1,000 pages / 10,000 tickets (deliberately, for ingest time
and shared-cluster politeness). The kit README explains the scaling
flags. Worth one sentence in the course intro or lab 0 so nobody
wonders why their index has 8,955 chunks, not millions. Also lesson 4.2
says the known issues index has "a few hundred records", the corpus
has 15. Consider softening to "a few hundred at most" or "a small,
exact set."

---

## 2. Fixed during the build (no action needed, listed for transparency)

- **SupportAI naming**: did not appear in either Word document's text
  (your Chapter 1 rename held), but the entire kit, corpus tarball,
  cluster resource names, and test spec were still branded. All renamed:
  kit → `example-corp-kit/`, corpus → `example-corp-corpus-v2.1.0`
  (data byte-identical to v2.0.0), cluster resources → `support-*`.
- **Old correction_loop.py bug**: it retried against `supportai-issues`
  and `supportai-tickets`, indexes that don't exist until Lab 4, so a
  Lab 3 learner could hit a 404 mid-demo. The new
  `scripts/correction_loop.py` filters by `doc_type` inside the single
  `support-docs` index instead, so Lab 3 only depends on Lab 1.
- **Python dependency removed from the learner path**: old labs
  required `pip install requests`. All lab scripts are now standard
  library only, and all infrastructure creation (pipelines, mappings,
  aliases) moved out of scripts into copy-paste `curl` in the labs, so
  learners see every request body.
- **Ingest robustness**: the loader now auto-resumes after
  interruption (stable chunk IDs make re-runs idempotent), retries on
  client timeouts with backoff, and paces batches to be polite on a
  shared cluster. Found this the honest way: the first full ingest run
  timed out client-side while the cluster was healthy.

## 2b. Technical findings from live validation (worth reading before recording)

- **The eval story on this corpus is "neural wins, fusion needs tuning,"
  not "hybrid wins."** Measured on the golden set (knowledge-base
  scoped), hit@5: BM25 ~0.50, neural ~0.63-0.64, hybrid-RRF 0.550,
  weighted 0.4/0.6 ~0.54, weighted 0.2/0.8 (tuned) ~0.61-0.62. The
  golden queries are customer-phrased (harvested from tickets), which
  favors the vector leg, and the default fusion dilutes it. Lab 1
  teaches this honestly and adds a tuning step (Step 12) demonstrating
  eval-driven improvement (0.550 -> ~0.61), exactly lesson 1.2's "prove
  it with the golden set" advice. But lesson 1.3's VO, if it claims
  hybrid tops the ablation table on camera, will contradict the
  numbers. Decide: adjust the VO framing, or ask me to rebalance the
  golden set's query-type mix (more error-code queries would push
  BM25/hybrid up; that's a new corpus version).
- **Eval metrics are reproducible to ~±0.02, not to the third
  decimal.** Two independent full runs proved the corpus's many tied
  BM25 scores and HNSW graph construction make exact reproduction
  across ingest histories impossible (a force-merge alone moved MRR by
  0.003). Labs and README now promise "within ~0.02, ordering always
  holds"; embedding vectors themselves ARE bit-identical (verified).
  If you want exact tables for the video, record the numbers from the
  cluster you film on, or ask me to add a deterministic tie-breaker to
  the eval script.
- **Eval must be knowledge-base-scoped.** Unscoped, ticket chunks
  (labeled never-relevant, phrased identically to the queries) flood
  the top-5 and every metric collapses to ~0.1. The eval script now
  has `--kb-only` and the lab explains why. If the videos show an
  unscoped ablation, the numbers will look broken.
- **Lesson 1.1's on-screen query "my dashboard takes forever to load"
  does not demo the BM25-fails story on this corpus**: real tickets
  contain that exact phrasing (BM25 nails it), and docs pages share
  "dashboard"+"load" vocabulary. The labs use "charts spin forever and
  never appear" (BM25 returns pagination/auth junk; neural returns
  "Troubleshooting dashboard rendering" at rank 1). Recommend the video
  demo use the same query, or keep the VO's phrasing as narration only.
- **ERR-2209 ticket resolutions all say "upgrade to 5.0."** So the
  course-script beat in 3.2 ("another 4.8 customer got through the same
  problem" via the ticket history) has no payoff in the data: for a 4.8
  customer there is genuinely no viable path, and the honest ending is
  LOW CONFIDENCE (which the kit README already calls the canonical
  demo). Lab 3 shows the ticket pivot firing and failing honestly, then
  demonstrates the CONFIDENT-via-ungated-workaround case with ERR-2288
  on 4.9. If you want the "a human wrote down what worked" beat to land
  literally, the generator needs a few pre-5.0 tickets with a
  non-upgrade resolution (new corpus version).
- **`_reindex` misbehaves on this 3.5.0 cluster**: intermittently
  returns `batches: 0` and copies nothing, no error reported. Lab 4
  therefore splits indexes with the bulk loader instead. Worth
  re-testing on 3.6 and possibly reporting to Instaclustr.
- **Template-corpus artifacts:** many generated pages tie on identical
  BM25 scores (e.g. all 50 integration guides score 5.97 on generic
  rotation queries), and integration-guide chunks rarely win over
  product-docs. Invisible in the labs as written, but avoid on-camera
  ad-lib queries; they can look odd.
- **Model deploy on medium nodes can return PARTIALLY_DEPLOYED** (one
  node's memory circuit breaker during warm-up). Predict still works; a
  second `_deploy` call completed it. Lab 0 documents this.

## 2c. Code-samples audit (on-camera snippets)

A dedicated consistency pass aligned `kit/code-samples/` with the
validated labs: fixed rename artifacts ("the the support tool"), stale
generator counts, a wrong `ingest_chunks.py` invocation, two cache
index bodies missing their `default_pipeline` (as written, embeddings
would never be populated), and cache `min_score` thresholds (0.90/0.93
were guesses; 1.7 is the live-validated value, real hit ~1.93, miss
~1.20). One judgment call for you: `lesson-2-2.md`'s ISM policy adds a
daily rollover + ism_template beyond Lab 2's simpler delete-only
policy. It's valid and reads as intentional "production-grade" teaching
detail; confirm you want the video and the lab to differ there.

## 3. Editorial issues in the Word documents

### Chapter 1 doc (`LP2_Chapter_1_Content_Revised.docx`)
- 1.1, "keyword, vector, sparse" segment: "This is where dense vector
  search **earns excels**", leftover from an edit; pick one verb.
- 1.1: "Lucene Better Binary Quantization, or BBQ **,** with", stray
  space before comma.
- 1.2: "It's also **expensive an expensive** operation" (reranking
  segment), duplicated word.
- 1.3: "strip the noise from the **boilerplatesm**", typo.
- 1.3: "This is where dense vector search" / "So **W**hich strategy
  should be used", mid-sentence capital.
- 1.3: "re-running a job should never **duplicates** anything" , 
  should be "duplicate."
- 1.4 has no explicit lab callout; the other chapters' code/demo
  moments map to kit samples. Consider adding "companion lab" pointers
  per lesson (the labs now exist per chapter).
- Header block still has placeholders: Learn Path Title empty, course
  summary "{To be written}", resources "TBC", FAQ "create as separate
  doc", all still open.

### Full course doc (`LP2_FULL_COURSE 2.docx`)
- 0.2 says "**One system, five chapters**" and the layer-cake visual
  labels the conclusion "**Ch5** Decision framework," but the course
  has four chapters plus a conclusion, and the conclusion's lessons are
  numbered 5.1/5.2. Consistent, but decide whether the conclusion is
  "chapter 5" or "the conclusion" and use one term in VO and visuals.
- 0.2: "Everything runs on OpenSearch 3.6 on the Instaclustr Managed
  Platform", see finding 1.1; true only once 3.6 is available there.
- 2.1 visual references "1.2 pre-filter discipline", the pre-filter
  lesson is 1.2 in the current numbering; verify it stays 1.2 if
  Chapter 1 is re-cut (the cut log shows 1.2/1.3 restructuring).
- 3.2: "the grader compares the customer's product version ... against
  the affected_versions and fixed_in_version fields sitting on the
  known issue chunk", matches corpus fields exactly. Good.
- 4.1: "at most five trips around ReAct" (4.3 says iteration ceiling 5)
 , consistent. Good.
- Word-count table checks out (10,314 total @125wpm = 82.5 min), but
  Chapter 1 is listed at 3,160 words / 25.3 min while the intro target
  in the Chapter 1 doc says 90 minutes for the whole path, the course
  is 82.5; fine, just confirm the "90 minutes" target line in the
  Chapter 1 doc header is stale.
- The five example tenants: 2.1 uses Northwind and Bluepeak. The labs
  use `northwind-logistics` / `bluepeak-financial` to match.

## 4. Validation summary (details in example-corp-kit/TEST_REPORT.md)

Two full validation passes were run:

1. **Build pass (me, while authoring):** every lab step executed live
   as it was written; expected outputs in the labs are real measured
   values from this cluster.
2. **Independent learner pass (fresh agent, wiped cluster):** all five
   labs executed literally, top to bottom, from a completely clean
   state. Result: **30 of 33 checkpoint assertions passed**, many
   byte-exact (embedding determinism values, all counts, score shapes,
   HyDE/msearch titles, cache hit/miss scores). It found 2 blocking
   bugs (a wrong expected output in Lab 2's skip-logic step; a missing
   brace in Lab 4's two answer-cache lookups), 2 misleading spots (the
   eval exactness promise; a Lab 4 step narrating fields the screen
   didn't show), and 4 smaller nits. All findings were fixed and the
   fixes re-validated live.
3. **Second independent pass on the LLM (Cohere) path (2026-07-10,
   fresh agent, wiped cluster again):** ALL FIVE LABS PASS: 28 of 30
   checkpoints clean, 2 pass-with-note, **zero blocking or misleading
   findings**. Every LLM behavioral checkpoint hit on the first try
   (rewrite, HyDE, grader verdict, both capstone RAG answers), all
   exact contracts held (determinism vector, counts, cache scores),
   and the eval ordering contract held with 11 of 12 cells within the
   stated ~0.02 tolerance (one cell at 0.021, covered by the lab's own
   variance explanation). The two friction notes (a transient
   `master key timed out` 500 on first connector create; remote models
   showing PARTIALLY_DEPLOYED) are now addressed in Lab 0's text.
   Current TEST_REPORT.md is this run's report.
