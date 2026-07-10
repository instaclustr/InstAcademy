# Chapter 2: RAG with Memory (script v2, validated 2026-07-10)

Rules carried over: 125 wpm pacing, spoken instructor voice, no em
dashes, every example drawn exclusively from the five Example Corp data
assets, explicit callbacks. Demo callouts reference the Example Corp
Data Kit labs (Lab 2 unless noted).

---

## 2.1 The Conversation Problem

### Title: 2.1: The Conversation Problem

**Voice over:**

Chapter one left the tool answering single questions well. Now watch it
fail. A customer asks: how do I fix ERR-2209? The tool retrieves the
known issue, explains the TLS 1.3 setting, cites the Snowflake guide.
Perfect. The customer replies: what about on version 4.9? And a
stateless pipeline embeds exactly those five words. What about on
version 4.9. No error code. No connector. No topic at all. Retrieval
returns noise, the model improvises over noise, and the system that
looked brilliant thirty seconds ago now looks broken. This is not an
edge case. Pull real threads from Example Corp's ticket history and you
will find the same shapes over and over. Pronouns: does it work with
SSO? Ellipsis: and on enterprise tier? Corrections: no, I meant the
analytics platform connector. Comparatives: is that faster than the old
way? Every one of these is unanswerable without the turns that came
before, and every one embeds into a meaningless vector on its own. That
is the conversation problem: real support interactions are threads, and
our pipeline only understands turns. This chapter fixes it in two
moves. First we give conversations a home in OpenSearch. Then we teach
the pipeline to use that history intelligently, without paying for it
on every turn.

**Visuals:**

- Title slide: "2.1: The Conversation Problem."
- Two turn replay: Turn 1 "how do I fix ERR-2209?" > cited answer.
  Turn 2 "what about on version 4.9?" > embedding of five context free
  words > junk results.
- Demo (Lab 2 Step 1): the actual turn-two junk on screen:
  "Troubleshooting mobile layouts," "Incremental Refresh overview,"
  "How email delivery works." Real output, real failure.
- Failure shape cards from real threads: pronoun / ellipsis /
  correction / comparative, each with a ticket style example.
- Caption: "threads, not turns."

### Conversation index design

**Voice over:**

The fix starts with storage, and conversations live in OpenSearch too,
in their own index. Each document is one message: a conversation ID, a
turn number, the role, the text, a timestamp, and the tenant. Keep the
mapping boring and exact: keyword fields for the IDs and role, a date
for the timestamp, text for the message. You will query this index by
conversation and by recency far more often than you will search it
semantically, so design for those access patterns first. Two choices
matter more than the rest. First, tenant isolation is not optional.
Northwind's conversation history must never leak into a Bluepeak
session, so tenant_id rides as a filter on every single read, the same
hard pre filter discipline you built in lesson 1.2, now applied to
memory. Treat a missing tenant filter on this index as a security bug,
not a quality bug. Second, store what you retrieved alongside what was
said. When the tool answers turn one, write the retrieved chunk IDs
onto that turn's document. Why? Because when turn two says what about
on version 4.9, the cheapest possible context is not re reading the
whole thread. It is knowing that turn one was answered from the
ERR-2209 known issue chunk and the Snowflake guide. Those chunk IDs are
breadcrumbs back to the topic, and they cost you nothing to keep.

**Visuals:**

- Mapping card for support-conversations: conversation_id (keyword),
  turn (integer), role (keyword), text, created_at (date), tenant_id
  (keyword), retrieved_chunk_ids (keyword).
- Access pattern note: "fetch by conversation + recency, not semantic
  search."
- Red X: cross tenant read. Green check: tenant_id filter on every
  query; badge "1.2 pre-filter discipline, applied to memory."
- Demo (Lab 2 Steps 2-3): the two-tenant read on screen: northwind
  returns 2 hits, bluepeak returns 0.
- Breadcrumb visual: turn 1 doc carrying chunk IDs > turn 2 resolution.

### Query rewriting & skip logic

**Voice over:**

Now the retrieval fix: query rewriting. Before embedding a follow up,
an LLM sees the recent conversation and rewrites the question so it
stands alone. Ask a real model to rewrite our follow-up and it produces
something like: how to enable TLS 1.3 in connector advanced settings
for version 4.9 to resolve ERR-2209 TLS handshake failure. Watch what
that rewrite accomplished. The error code is back, so the BM25 leg has
something to bite. The topic is back, so the vector leg lands in the
right neighborhood. And the version number appeared, which your 1.2
pre filters can enforce as a hard constraint. One rewrite repaired all
three retrieval paths at once. But rewriting costs a model call on
every turn, and here is the thing: most turns do not need it. First
questions usually stand alone. Many follow ups do too. So add skip
logic in front. Only rewrite when the query shows dependence on
context: pronouns like it, that, this one. Short fragments. References
like the second option or the same error. A cheap check catches these,
regex or a tiny classifier, and in practice the rewriter fires on maybe
a third of turns. That means two thirds of your traffic skips an entire
LLM call, which at Example Corp's volume is real latency and real
money. This is a pattern to tattoo somewhere visible, because the whole
course repeats it: spend intelligence only where the query needs it.
Next lesson: the history that rewriting depends on grows without limit,
and prompts do not.

**Visuals:**

- Before/after: "what about on version 4.9?" > rewriter (sees history +
  turn 1 chunk IDs) > standalone query; three repair badges: BM25 leg
  (code restored) / vector leg (topic restored) / pre-filter (version
  extracted).
- Demo (Lab 2 Step 5): the LIVE model rewrite on screen: "How to enable
  TLS 1.3 in connector advanced settings for version 4.9 to resolve
  ERR-2209 TLS handshake failure?" then the repaired retrieval. Caveat
  chip: "your model's wording will differ; the repairs will not."
- Skip gate: pronoun / fragment / reference detector; two exits:
  rewrite (~1/3 of turns) vs straight to retrieval (~2/3).
- Cost chip: "an LLM call saved on the majority path, 500 tickets a
  day."
- Principle banner: "spend intelligence only where the query needs it."

---

## 2.2 Memory Strategies & Token Management

### Title: 2.2: Memory Strategies & Token Management

**Voice over:**

Rewriting needs history, and history grows. A gnarly Example Corp
escalation can run forty turns across three days: symptoms, screenshots
described in text, two wrong guesses, a workaround, a regression. You
cannot ship forty turns into every prompt, and you would not want to if
you could, because half of it is noise now. Memory strategy is deciding
what the model gets to remember, and there are three basic designs.
Sliding window: keep the last N turns verbatim. It is simple, it is
perfectly faithful for recent context, and it is completely forgetful.
The error code established in turn two is gone by turn twenty, and the
customer should not have to repeat it. Summary memory flips the
tradeoff: periodically compress older turns into a running summary that
rides in the prompt. Now the thread's whole plot survives cheaply, but
details blur in compression, and blurred details are exactly what a
support assistant cannot afford. A summary that remembers a connector
issue on version 4 point something is a summary that gets the customer
a wrong answer. So production systems run the hybrid: a compact summary
of everything old, plus the last few turns verbatim. The summary holds
the plot. The window holds the details. When the tool drafts a reply on
turn thirty, it knows the thread started with ERR-2209 on the Snowflake
connector, and it has the customer's exact last three messages word for
word.

**Visuals:**

- Title slide: "2.2: Memory Strategies & Token Management."
- Forty turn escalation thread trying to fit a prompt box.
- Three strategy cards: Sliding window (faithful, forgetful: turn 2
  error code lost by turn 20) / Summary (long memory, blurry details:
  "version 4 point something") / Hybrid (summary of the old + verbatim
  recent), hybrid card glows.
- Split prompt visual: summary block + last 3 turns verbatim.

### Token budgets & session lifecycle

**Voice over:**

Make the budget explicit, in writing, in the repo. Say the tool packs
eight thousand tokens of context per request. Split it deliberately:
roughly half for retrieved chunks, a quarter for conversation memory,
and the rest for instructions and headroom. The exact ratios are yours
to tune, but the rule underneath them is not negotiable: when memory
wants more than its share, summarize harder. Never let history crowd
out retrieved evidence, because the evidence is what keeps answers
grounded, and a model with lots of memory and thin evidence drifts back
to improvising. Then manage the lifecycle, because conversations are
data with an expiry date. Use Index State Management policies, ISM, to
handle it inside the cluster: roll conversation indexes on a schedule,
and delete sessions past your retention window, thirty days, ninety
days, whatever your compliance posture says. Quick terminology note if
you come from Elasticsearch: your fingers will type ILM, but in
OpenSearch the feature is ISM, Index State Management. Same job,
different name, and your automation will care about the difference. And
one more time, because this index is user data: every memory read
filters on tenant_id, multi user isolation is enforced at the query
layer, and retention applies per tenant if your contracts differ.
Memory earns the same access discipline as the document index, not
less.

**Visuals:**

- Token budget donut: ~50% retrieved chunks / ~25% memory / ~25%
  instructions + headroom; rule "memory never crowds out evidence."
- ISM lifecycle rail: active conversations > rollover > delete at
  retention window. Terminology chip: "Elasticsearch ILM = OpenSearch
  ISM."
- Demo (Lab 2 Step 8): the support-conversation-retention ISM policy
  created live.
- Multi user isolation badge on the memory read path; per tenant
  retention note.

### ML Commons Memory API

**Voice over:**

You can build all of this by hand, and now you understand exactly what
it costs to build. But OpenSearch also ships memory as a platform
feature. The ML Commons Memory API stores conversations and their
messages natively in the cluster, and the conversational search
pipeline can carry a memory ID, so context handling happens server side
instead of in your application code. And in 3.6 the agent framework
pushes this further, with agentic memory that carries context across
interactions, which we will lean on directly in chapter four. So which
do you choose? Honest answer: it depends what you need to control. The
native API is less code, fewer moving parts, and it evolves with the
platform. The custom conversation index gives you full control over the
pieces this chapter just taught you to care about: exactly how
rewriting sees history, exactly how summarization compresses, exactly
what enters the prompt and in what order, and exactly how tenant
isolation is enforced. For our support tool we build custom in the
labs, because you cannot evaluate a managed abstraction until you
understand the mechanics underneath it. The graduation criterion is
simple: adopt the native API the day its defaults match the design you
now know how to specify.  Next lesson, we go beyond conversation
entirely, because follow ups are not the only queries that arrive
broken.

**Visuals:**

- Split panel: "Build it" (custom conversation index: full control of
  rewriting, summarization, prompt assembly, isolation) vs "Use the
  platform" (ML Commons Memory API + conversational pipeline with
  memory ID: less code, evolves with OpenSearch).
- 3.6 badge: agentic memory in the agent framework, arrow "chapter 4."
- Decision line: "adopt native when its defaults match your spec."
- Demo (Lab 2 Step 9): create memory + message via ML Commons Memory
  API, side by side with the custom index write.

---

## 2.3 Beyond Chat: Query Enhancement Patterns

### Title: 2.3: HyDE for vague queries

**Voice over:**

Rewriting fixed follow ups. But some queries arrive broken in other
ways, even as first questions, and this lesson adds two more
enhancement tools plus the routing logic that keeps them affordable.
Tool one: HyDE, hypothetical document embeddings, for vague queries. A
customer writes: dashboards are acting weird lately. Embed that
sentence and you get a vague vector, and here is what it actually
finds: other customers complaining that dashboards are acting weird.
The problem, restated three ways, and not one answer. Vague customer
phrasing lands in the neighborhood of other vague customer phrasing.
HyDE's trick is almost cheeky: ask the LLM to imagine the documentation
passage that would answer the question, and embed the imaginary passage
instead. For our query, the model drafts a couple of sentences in
documentation voice about dashboard rendering inconsistencies and how
to address them. That draft is fiction, but it is fiction written in
the vocabulary of the real docs, and in vector space it lands inside
the docs cluster: the top results flip from three tickets to the
dashboard rendering troubleshooting pages, the actual answer. You
retrieve with the hypothetical, then generate from the real chunks you
found. The fake document never reaches the customer; it exists only to
aim the search. HyDE costs one LLM call and buys you retrieval on
queries that were previously hopeless. Which immediately raises the
question we keep meeting: do you want to pay that call on every query?
Hold that thought for two minutes.

**Visuals:**

- Title slide: "2.3: Beyond Chat: Query Enhancement Patterns."
- HyDE flow: "dashboards are acting weird lately" > LLM drafts a
  hypothetical docs passage > embed the hypothetical > retrieve real
  chunks > generate from real chunks only.
- Demo (Lab 2 Step 6): the before/after on screen. Before: three
  "Dashboard takes forever to load" tickets. After: "How dashboard
  rendering works," "Troubleshooting dashboard rendering," "Dashboard
  Rendering settings reference." Caption: "the problem vs the answer."
- Vector space sketch: vague query inside the complaints cluster,
  hypothetical inside the docs cluster.
- Cost chip: "+1 LLM call. Worth it? Hold that thought."

### Query decomposition via _msearch

**Voice over:**

Tool two: decomposition, for compound questions. A customer asks: does
the Salesforce connector support OAuth, and how do I rotate the
credentials? That is two questions wearing one trench coat. Embed it
whole and you get an average of two topics, a vector pointing between
the OAuth section and the rotation section, retrieving mediocre results
for both halves. Branched RAG splits it: an LLM decomposes the compound
question into standalone sub queries, and here OpenSearch gives you a
beautiful primitive, _msearch. One request, one body, multiple
independent searches executed in a single round trip. Sub query one,
Salesforce OAuth support, hits the authentication section of the
Salesforce guide and the ERR-2231 known issue about expired refresh
tokens. Sub query two, credential rotation, hits the connector
credential rotation pages. Merge the two result sets, deduplicate on
chunk ID, and the generation prompt receives complete evidence for both
halves of the question, clearly attributable to each. The pattern
generalizes past the trench coat case. Comparisons are decompositions
too: customers constantly ask how the Snowflake and BigQuery connectors
differ, and the honest retrieval for that is two searches, one per
connector, not one search for a comparison document that probably does
not exist. Any time a question contains an and, an or, or a versus,
your retrieval should at least consider splitting.

**Visuals:**

- Trench coat visual: one compound question splits into two standalone
  sub queries.
- One _msearch body > two parallel searches > merged, deduplicated
  context pack with per sub query attribution.
- Demo (Lab 2 Step 7): _msearch with two queries against support-docs,
  results labeled per sub query: block one is ERR-2231 and the
  Salesforce guide, block two is the Connector Credential Rotation
  pages.
- Second example: "Snowflake vs BigQuery connector" > two searches, one
  per connector.
- Heuristic chip: "and / or / versus = consider splitting."

### Adaptive triggering & chapter close

**Voice over:**

Count the tools now: query rewriting from lesson 2.1, HyDE,
decomposition. Each one is an extra LLM call, and if you run all of
them on everything, you have built a system that does maximum work on
every query regardless of need. At Example Corp's volume, five hundred
tickets a day plus follow ups, always on enhancement is a cloud bill
with a search engine attached. So route, cheaply. A small
classification pass in front of the pipeline, rules or a lightweight
model, tags each incoming query. Context dependent, pronouns and
fragments? Rewrite. Vague, no technical vocabulary, no error code?
HyDE. Compound, an and or a versus joining two askables? Decompose. And
clean, specific, standalone, which is honestly most of Example Corp's
traffic, thanks to customers who paste error codes? Straight through to
the chapter one pipeline, untouched, at full speed. The triggering
logic itself must stay cheap: if your router costs as much as the
enhancement it gates, you have gained nothing. Rules and regex go
surprisingly far here; an ERR pattern match is free and unambiguous.
Now step back and look at what we just built, because it matters for
where this course is going. There is a small decision maker sitting in
front of the pipeline, reading each query and choosing a strategy.
Chapter four takes that seed and grows it into a full agent. But first,
chapter three, and an uncomfortable question we have been walking past:
all of this assumes retrieval returns good chunks. What happens when it
does not?

**Visuals:**

- Router diagram: query > cheap classifier > four lanes: rewrite / HyDE
  / decompose / straight through (widest lane, "most traffic").
- Cost meter: always on enhancement vs adaptive triggering at 500
  tickets/day.
- Rule chip: ERR pattern match = free routing signal.
- Foreshadow card: "a decision maker in front of the pipeline > chapter
  4 makes it an agent."
- Handoff: "what if retrieval itself is wrong?" > chapter 3.

---

## Change log vs the current draft (for review)

1. **2.1 rewriting segment:** the example rewrite is now the one a real
   model produced during validation ("how to enable TLS 1.3 in
   connector advanced settings for version 4.9...") instead of the
   invented one, with a visuals caveat chip that wording varies. Also
   "Fragments, those five word replies" became "Short fragments"
   (the validated skip gate uses a four-word threshold; five-word
   fragments are caught by the reference regex, so the old phrasing
   taught the wrong rule of thumb).
2. **2.1 and 2.2:** "data warehouse guide" tightened to "Snowflake
   guide"/"Snowflake connector" where the demo shows Snowflake
   specifically (the corpus names it; VO and screen now agree).
3. **2.3 HyDE segment:** rewrote the middle to match what the demo
   actually shows: the vague query retrieves other complaints (tickets),
   not "everything and nothing," and HyDE flips results to the docs.
   This is a stronger, validated story: "the problem vs the answer."
4. **2.3 decomposition:** "CRM connector" became "Salesforce connector"
   to match the on-screen demo, and the sub-query results now match
   validated output (sub query one carries the ERR-2231 known issue;
   sub query two hits the credential rotation pages). Comparison
   example updated from "data warehouse vs analytics platform" to
   "Snowflake vs BigQuery" for the same reason.
5. **Demo callouts** throughout now reference specific lab steps and
   real validated outputs, so the editor can pull screen captures
   directly from a lab run.
6. No changes to 2.2's teaching content; only the lab callouts were
   added.
