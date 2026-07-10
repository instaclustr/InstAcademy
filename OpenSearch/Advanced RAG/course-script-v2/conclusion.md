# Conclusion (script v2, validated 2026-07-10)

Rules carried over: 125 wpm pacing, spoken instructor voice, no em
dashes, explicit callbacks.

---

## 5.1 The Decision Framework

### Title: 5.1: The Decision Framework

**Voice over:**

You now have four patterns and one dangerous instinct: to use all of
them everywhere. Resist it. Every layer in this course buys quality
with cost and latency, and the real engineering skill is not building
the layers, it is knowing which trigger you have actually hit. So here
is the decision path, and notice it is ordered. Every system starts as
chapter one: hybrid retrieval, disciplined ingestion, a golden set,
dashboards. And you do not leave this stage until retrieval metrics are
healthy, because this is the load bearing rule of the whole course:
nothing downstream fixes bad retrieval. Memory cannot remember its way
past missing chunks, correction can only reshuffle what retrieval can
reach, and an agent orchestrating weak indexes is just expensive noise.
Add memory when your logs show real multi turn behavior: follow ups
failing, pronouns hitting a stateless pipeline, users repeating context
they already gave. If your traffic is genuinely single shot, and some
search applications are, memory is pure overhead. Add corrective RAG on
either of two triggers: your traces show confident answers built on
weak evidence, our version mismatch case, or the cost of one wrong
answer is high. For customer facing support, it usually is, which is
why most systems like this one want this layer early. Add agents last,
and only when queries genuinely diverge in what they need: multiple
sources, different strategies per question shape, whole categories
visibly underserved by one pipeline. If a router plus one good pipeline
serves your traffic, stop there; agency you do not need is cost and
failure surface you do not need.

**Visuals:**

- Title slide: "5.1: The Decision Framework."
- Ordered decision tree: healthy Ch1 metrics gate (load bearing rule
  banner: "nothing downstream fixes bad retrieval") > multi turn
  failures in logs? add memory > weak evidence answers or high wrong
  answer cost? add CRAG > divergent query needs, multi source? add
  agents; else stop.
- Anti-pattern chips: memory on single shot traffic / agency without
  divergence.
- Trigger table: pattern / observable signal / what it costs.

### Combinations & the cost spectrum

**Voice over:**

The layers also combine in predictable pairs, and knowing the common
combinations saves you design meetings. Memory plus corrective is the
conversational assistant that checks itself: it holds the thread and it
verifies evidence before answering. Most production support bots, ours
included, should live here or aspire to. Agent plus corrective is the
research grade combination: every tool call graded, weak evidence
reformulated mid loop, the chapter four tool wrapper pattern. Reach for
it when questions are genuinely investigative. And if you later extend
into graph augmented retrieval, relationships between entities rather
than similarity between chunks, graph plus agent is its natural
pairing, with the agent deciding when to traverse relationships and
when to search text; that is beyond this course, but the decision logic
you now own transfers directly. Keep the cost quality latency spectrum
on one slide in your head. Base RAG: cheapest, fastest, one retrieval
and one generation. Memory adds rewriting calls and prompt tokens.
Correction adds grading calls and up to two retries on the hard cases.
Agents add loops of everything, bounded only by the ceilings you set.
Each step right on that spectrum should be paid for by a measured
quality gain on your golden set, not by enthusiasm. You watched that
discipline work at the very bottom of the stack, where one measured
fusion change beat the default, and it works the same at every layer
above. The honest way to know a trigger fired is the instrumentation
you built in chapter three: let the dashboards promote your
architecture, one layer at a time, with evidence.

**Visuals:**

- Combo cards: Memory + CRAG ("the support bot sweet spot, our build
  lives here") / Agent + CRAG (research grade, tool wrapper pattern) /
  Graph + Agent (future extension, traversal vs search).
- Cost quality latency spectrum bar: base RAG > +memory (rewrites,
  tokens) > +correction (grading, retries) > +agents (bounded loops of
  everything).
- Rule banner: "each step right is paid for by measured golden set
  gains."
- Callback chip: the Lab 1 fusion tuning result as the miniature
  example of evidence-driven promotion.
- Dashboards promote architecture visual (3.3 callback).

---

## 5.2 Your Action Plan

### Title: 5.2: Your Action Plan

**Voice over:**

Let's make Monday morning concrete, three steps. Step one: stand up
chapter one for real, on your data. Identify your own five assets,
whatever your equivalents of docs, guides, tickets, known issues, and
API reference are; every organization has them, usually scattered. Run
the ingestion discipline from lesson 1.3: parse for structure, chunk
per asset type, stamp the metadata, and build a golden set of a couple
hundred labeled queries before you write a single prompt. If you take
one habit from this course, take that ordering: evaluation exists
before generation does. Step two: instrument before you extend. Stand
up the traces index and the retrieval dashboards from lesson 3.3 while
the system is still simple, because every upgrade decision you will
ever make should come from that data, and retrofitting observability
into a complex agent system is miserable work you can simply skip by
starting now. Step three: climb the layers on triggers, in the order
the decision framework gave you, and measure each layer against the
same golden set as you go, so improvement is a number and not a
feeling. From here, three directions are worth your reading time. Self
RAG, where the model itself learns to critique and gate its own
retrieval, correction moving inside the model. Multimodal RAG, because
Example Corp's docs are full of screenshots and dashboard images your
text embeddings currently walk straight past, and so are yours. And the
HyDE variants and query enhancement literature, which keeps producing
cheap retrieval wins for the price of a paper a week. Resource links
for all three are below this video, along with the companion labs on
the Instaclustr Managed Platform, which run every demo you watched on
the exact Example Corp dataset. The labs work two ways: bring a free
LLM API key and run the full system live, model and all, or run the
no key path and perform the model's moves by hand; either way, your
retrieval numbers land where the course said they would, because same
data, same model, same math. You did not just learn four patterns. You
built one system, layer by layer, and measured every step of it. Now go
build yours.

**Visuals:**

- Three step roadmap: (1) Ch1 on your data: find your five assets, 1.3
  ingestion discipline, golden set FIRST (habit banner: "evaluation
  before generation") > (2) instrument early: traces + dashboards while
  simple (3.3) > (3) climb on triggers, measure every layer on the same
  golden set.
- Beyond this course cards: Self RAG (correction moves inside the
  model) / Multimodal RAG (screenshots your embeddings walk past) /
  HyDE variants and query enhancement.
- Resource links panel + companion labs badge (Instaclustr Managed
  Platform, exact Example Corp dataset). Two-path chip: "free LLM key,
  or no key at all."
- Closing slide: the full stack layer cake, "now go build yours."

---

## Change log vs the current draft (for review)

1. **5.1 combinations segment:** added one sentence connecting "paid
   for by measured golden set gains" to the validated Lab 1 fusion
   tuning result, so the principle has an on-screen receipt from the
   learner's own hands.
2. **5.2:** "two hundred labeled queries" softened to "a couple hundred
   labeled queries" (the course's own golden set is 300; the advice is
   about the learner's data, so a round number reads better than a
   specific one that differs from what they just used). The companion
   labs sentence now describes the two paths (free LLM key or no-key)
   and repeats the determinism promise in its validated form.
3. Everything else in the conclusion is unchanged from the draft except
   punctuation (no em dashes anywhere in v2 scripts).
