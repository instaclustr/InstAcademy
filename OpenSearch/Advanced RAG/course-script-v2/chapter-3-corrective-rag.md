# Chapter 3: Corrective RAG (script v2, validated 2026-07-10)

Rules carried over: 125 wpm pacing, spoken instructor voice, no em
dashes, every example from the five Example Corp data assets, explicit
callbacks. Demo callouts reference the Example Corp Data Kit labs
(Lab 3 unless noted).

---

## 3.1 Why Retrieval Quality Is Everything

### Title: 3.1: Why Retrieval Quality Is Everything

**Voice over:**

Here is the failure that motivates this whole chapter, and it is
sitting in our own corpus, waiting. A customer on version 4.8 hits
ERR-2209, the connector handshake failure. The tool retrieves
confidently: the known issue record is right there, and it says enable
TLS 1.3 in the connector advanced settings. Clean retrieval, high
score, fluent answer, source cited. One problem. That setting shipped
in version 5.0. The customer is on 4.8, where the advanced settings
panel does not contain it. The support agent sends the fix, the
customer stares at a screen with no such option, and now there are two
tickets where there was one. Walk the autopsy with me, because the
diagnosis is the whole chapter. The retrieval was relevant: ERR-2209
was exactly the right topic. The generation was faithful: the model
accurately summarized the chunk it was given. Nobody hallucinated. The
system simply never asked whether the evidence fit this customer. Their
version was sitting in the ticket metadata the entire time, and the
known issue chunk carried affected versions and fixed in version
fields, and no stage of our pipeline ever compared them. That is the
uncomfortable truth of production RAG: retrieval is the dominant
failure mode, and it fails in ways more subtle than returning nothing.
It returns the almost right thing. Garbage in does not look like
garbage. It looks like a polished, cited answer that happens to be
impossible to follow.

**Visuals:**

- Title slide: "3.1: Why Retrieval Quality Is Everything."
- The version mismatch replay: 4.8 customer > ERR-2209 > retrieved fix
  requires 5.0 > agent screen with no such setting > two tickets where
  there was one.
- Demo (Lab 3 Step 1): the actual known issue chunk on screen, reading
  the lines aloud-able: "Workaround: Enable TLS 1.3 in the connector
  advanced settings, available in 5.0 and later. Affected versions:
  4.8, 4.9. Fixed in: 5.0."
- Autopsy panel: retrieval relevant (check) / generation faithful
  (check) / evidence fits customer (never checked, red).
- Side by side metadata that never met: ticket product_version 4.8 vs
  chunk fixed_in_version 5.0.
- Caption: "garbage in looks like a polished, cited answer."

### _score and _explain as diagnostics

**Voice over:**

Before we build the fix, learn to see the failure, because OpenSearch
hands you two diagnostic signals for free and most teams ignore both.
The first is _score, and the information is not in any single number,
it is in the shape of scores across the result list. A healthy
retrieval has separation: a clear leader, then a visible drop, then the
long tail. That shape says something specific matched. A sick retrieval
is flat: eight results huddled in a narrow band, which usually means
nothing really matched and you are looking at the eight least
irrelevant chunks in the index. Train your eye on relative shape, not
absolute values, because absolute scores are not comparable across
query types, and BM25 scores versus fused hybrid scores live on
entirely different scales. Flat and low is a retrieval alarm you can
compute in one line, and it becomes our cheapest correction trigger
next lesson. The second signal is _explain. Add explain true to a query
and OpenSearch decomposes exactly why each document scored what it
scored: which terms matched in which fields, what each clause
contributed, how the pieces combined. When the wrong chunk wins,
_explain tells you whether the query put it there, the chunking put it
there, or a field weight put it there. In our version mismatch case,
_explain would show a perfectly healthy lexical match on ERR-2209,
which is precisely the point: score diagnostics catch weak retrieval,
but they cannot catch relevant retrieval that fails the customer's
context. For that we need a grader that reads. These two signals are
your debugging eyes. The correction loop we build next simply automates
the looking, and adds the reading.

**Visuals:**

- Two score distributions, the real ones from the demo cluster:
  healthy `2.92  2.21  2.21  2.21  2.18 ...` (leader + cliff + tail) vs
  sick `1.74  1.74  1.74  1.74  1.73 ...` (flat huddle); label "shape,
  not absolute value; scales differ across query types."
- One line alarm chip: "flat AND low = correction trigger (next
  lesson)."
- _explain output annotated: term matches, per clause contributions,
  combination, for a wrong winner.
- Limit card: _explain shows a healthy ERR-2209 match in the mismatch
  case > "scores catch weak retrieval, not wrong fit; that needs a
  grader."
- Demo (Lab 3 Steps 2-3): the two score lists and the explain tree,
  live.

---

## 3.2 Building the Correction Loop

### Title: 3.2: Building the Correction Loop

**Voice over:**

Corrective RAG adds exactly one question between retrieval and
generation: is this evidence actually good enough to answer from?
Everything in this lesson is machinery for asking that question cheaply
and acting on the answer. We grade in two passes, cheap pass first.
Pass one is the _score gate, pure OpenSearch, effectively free, running
the shape check from last lesson. Three exits. If the top result clears
a healthy threshold with real separation, proceed straight to pass two
with high confidence, or on easy queries, skip grading entirely. If the
whole list is flat and low, do not waste an LLM call grading garbage:
jump directly to correction, because we already know retrieval missed.
And the middle band, plausible but uncertain, goes to pass two. Pass
two is the grader, and its power is that it reads. For each candidate
chunk it answers narrow, specific questions. Does this chunk actually
address the question asked? And does it fit the customer's context?
That second check is the one that catches our 4.8 customer being handed
a 5.0 fix, and notice how it works: the grader compares the customer's
product version, which rides in from the ticket, against the affected
versions and fixed in version facts sitting on the known issue chunk.
Fields you stamped during ingestion in lesson 1.3, back when they
looked like bookkeeping. Metadata discipline in chapter one just became
correction signal in chapter three. And one subtlety the real corpus
teaches: read the workaround too. Our known issue has a workaround, but
the workaround itself says available in 5.0 and later. A grader that
stops at "workaround exists" passes a chunk this customer still cannot
use. Keep the grader's job narrow, its prompts short, and its verdicts
structured: pass, fail, and a machine readable reason, because the next
stage acts on that reason.

**Visuals:**

- Title slide: "3.2: Building the Correction Loop."
- Two pass gate: Pass 1 _score shape gate (free) with three exits:
  proceed / grade / straight to correction. Pass 2 grader on the middle
  band.
- Grader card reading chunk facts: affected versions 4.8, 4.9 + fixed
  in 5.0 + workaround gated "available in 5.0 and later" vs
  customer_version 4.8 > FAIL: version fit, structured reason attached.
- Demo (Lab 3 Step 4b): the live LLM grader verdict on screen:
  `{"pass": false, "reason": "The customer is on version 4.8, and the
  workaround requires version 5.0 or later."}`
- Callback badge: "1.3 metadata pays off here."
- Verdict format chip: pass / fail / machine readable reason.

### Correction strategies & retry budget

**Voice over:**

So the grade came back weak. Now the loop earns its name, with three
moves in escalating order, each driven by the grader's reason. Move
one: reformulate the query. If the failure was topical, expand ERR-2209
with its human title, connector handshake failed, so the lexical leg
has more to match. If the failure was version fit, add the customer's
version as a hard filter, the 1.2 pre filter, so content that cannot
apply to them stops entering the candidate set. Move two: change where
you look. If the docs failed our 4.8 customer, the ticket history is
the natural second source, because somewhere in two hundred thousand
tickets, another 4.8 customer hit ERR-2209 and a human wrote down how
it actually ended. Different asset, different retrieval strategy, same
question. Now watch what happens when we run this exact case, because
the ending matters. The version filter still surfaces the same 5.0
gated fix. The ticket pivot finds the humans' answer, and the humans'
answer was: upgrade to 5.0. For a customer who cannot upgrade today,
there is no viable fix in the entire corpus, and that is the truth.
Which brings us to move three, and it is not really a move, it is the
discipline that keeps the whole thing shippable: a retry budget, and
ours is two. Retrieve, correct, correct once more, done. Without a hard
ceiling, a genuinely unanswerable query loops forever, and your four
hour SLA dies in a retry storm of LLM calls. And when the budget is
spent and the evidence is still weak? Do not fake it. Signal confidence
to the generation prompt: tell the model the evidence is partial,
instruct it to say clearly what is known and what is not, and route the
ticket to a human with the trail attached. Our 4.8 customer gets: the
fix exists, it requires 5.0, here is who can help you plan the upgrade.
A support assistant that says I am not certain, here is what I found,
and here is who can help, builds trust with every miss. One that
guesses burns trust with every hit, because nobody knows which answers
to believe. And so you see both endings in the labs: ERR-2209 on 4.8
ends in an honest low confidence handoff, while ERR-2288, whose
workaround has no version gate, sails through for a 4.9 customer on the
first pass. Same loop, opposite verdicts, and both of them right.

**Visuals:**

- Escalation ladder driven by grader reasons: (1) Reformulate: expand
  code with title / add version pre-filter > (2) Pivot source: ticket
  history ("a human wrote down how it ended") > (3) Hard stop: retry
  budget = 2.
- Demo (Lab 3 Step 4): the full 4.8 run on screen, attempt by attempt:
  version-fit FAILs > version filter > still gated > ticket pivot >
  tickets say "upgrade to 5.0" > LOW CONFIDENCE, honest handoff.
- Contrast demo: the 5.1 run and the ERR-2288 on 4.9 run, both
  CONFIDENT after zero corrections.
- Loop diagram with exit gate after two corrections; anti-pattern X:
  retry storm vs 4 hour SLA.
- Confidence signaling: prompt banner "evidence partial" > answer
  states knowns and unknowns > escalate with trail.
- Trust ledger visual: honest miss builds trust / confident guess burns
  it.

---

## 3.3 Evaluating Your RAG System

### Title: 3.3: Evaluating Your RAG System

**Voice over:**

Chapter one measured retrieval with hit rate, precision, and MRR on the
golden set, and those metrics still run underneath everything. But
corrective RAG needs the next layer up, because now the interesting
question is not did we find the chunk, it is did the whole system
produce a good answer, and did the correction loop actually help. Four
questions frame system level evaluation. Context relevance: of the
chunks we handed the model, how many actually mattered to the question?
This is precision's system level cousin, and it tells you whether your
pipeline packs signal or noise. Faithfulness: does the generated answer
follow from the retrieved chunks, or did the model add claims with no
support? Faithfulness failures are the scariest class, because they
reintroduce hallucination through the back door of a working retrieval
system. Answer correctness: judged against a reference answer, is it
right? For our support tool, references come cheap: resolved tickets
carry the answer a human eventually gave. And underneath, your
retrieval metrics from lesson 1.3, because when faithfulness drops, the
first suspect is always what got retrieved. You do not have to build
the harness from scratch. RAGAS is an open source framework that
computes exactly these metrics, using LLM as judge: a model reads the
question, the retrieved context, and the answer, and scores relevance
and faithfulness at a scale no human team can match, across every one
of its responses, every day. But calibrate the judge before you trust
it. Sample a slice, have your support leads score the same answers, and
measure agreement. An uncalibrated judge is a dashboard that lies with
confidence, which is exactly the failure mode this chapter exists to
kill.

**Visuals:**

- Title slide: "3.3: Evaluating Your RAG System."
- Metric stack: retrieval layer (hit rate / precision / MRR, 1.3
  callback) under system layer: context relevance / faithfulness /
  answer correctness.
- Faithfulness warning card: "hallucination through the back door."
- Reference source: resolved tickets = free reference answers.
- RAGAS + LLM as judge diagram with calibration loop: human sample vs
  judge scores > agreement check.
- Caption: "an uncalibrated judge lies with confidence."

### OpenSearch as the observability layer

**Voice over:**

Now the move that turns evaluation from a quarterly report into an
operational tool: store it all in OpenSearch itself. Every support
request already flows through the cluster, so log one trace document
per request into a traces index: the original query, the rewrite if
lesson 2.1 fired, the retrieved chunk IDs and their scores, the grader
verdicts and reasons, the retry count, the final RAGAS metrics, and
latency per stage. Now your RAG system is a set of dashboards, and the
questions that used to take a data export take a query. Which product
areas grade worst this week? Filter traces by product_area, aggregate
faithfulness. Did the correction loop actually improve answers, or just
add latency? Compare metrics on traces with retries against traces
without. What does the retry budget cost at p95? It is a percentile
aggregation away. The search engine you already run becomes its own
observability layer, and quality regressions show up as chart movements
days before they show up as angry escalations. Then close the loop with
the humans you already employ. Support agents review every draft before
it ships: each acceptance is a positive label, each edit is a
correction with a diff, and each rejection is a hard negative. That
stream flows back into the golden set from lesson 1.3, which means your
evaluation data grows and stays current as Example Corp ships new
versions and new error codes appear. Retrieval, correction, evaluation,
feedback: the loop is closed and it is self improving. Next chapter, we
hand this well instrumented system the steering wheel.

**Visuals:**

- Trace document mock: query, rewrite, chunk_ids + scores, grader
  verdicts + reasons, retries, RAGAS metrics, latency per stage >
  support-traces index.
- Demo (Lab 3 Step 5): the traces index and the
  faithfulness-by-product-area aggregation, live.
- OpenSearch Dashboards mock: faithfulness by product area / correction
  lift vs latency cost / retry cost at p95.
- Feedback loop: agent accepts (positive label) / edits (correction +
  diff) / rejects (hard negative) > golden set refresh (1.3 callback).
- Caption: "regressions as chart movements, not angry escalations."
- Handoff: "now hand it the steering wheel" > chapter 4.

---

## Change log vs the current draft (for review)

1. **3.2 grading segment:** added the validated corpus subtlety that
   the WORKAROUND itself is version gated ("available in 5.0 and
   later"), so a grader that stops at "workaround exists" still fails
   this customer. This is real, it is in the data, and it deepens the
   "grader that reads" point. The grader demo callout now shows the
   live LLM verdict from validation.
2. **3.2 correction segment (the big change):** the old draft promised
   the ticket pivot would find "what actually worked" for a pre-5.0
   customer. In the corpus, every resolved ERR-2209 ticket ends in
   "customer upgraded to 5.0," so that beat had no payoff on screen.
   Rewritten so the flagship 4.8 demo ends in the honest LOW CONFIDENCE
   handoff (which the narration then celebrates as the point), and
   ERR-2288 on 4.9 provides the on-screen contrast where an ungated
   workaround sails through. Both endings are validated demos in Lab 3.
   The "escalating three moves" framing is preserved; move two is now
   "change where you look" (the query-noise-stripping sub-case was cut
   for time and because no demo exercises it).
3. **3.1 score shapes:** "ten results huddled" became "eight results
   huddled" to match the on-screen demo (size 8), and the visuals now
   carry the real score lists (2.92/2.21... vs 1.74/1.74...) so the
   editor can label the exact frames.
4. **Demo callouts** throughout now point at specific Lab 3 steps with
   validated outputs.
5. 3.3 is unchanged except demo callouts; note RAGAS itself is
   discussed but not exercised in the labs (it needs a Python
   environment beyond the stdlib-only rule); the traces/dashboard
   machinery it feeds IS demoed live.
