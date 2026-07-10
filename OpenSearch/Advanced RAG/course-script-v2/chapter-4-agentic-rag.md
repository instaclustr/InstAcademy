# Chapter 4: Agentic RAG (script v2, validated 2026-07-10)

Rules carried over: 125 wpm pacing, spoken instructor voice, no em
dashes, every example from the five Example Corp data assets, explicit
callbacks. Demo callouts reference the Example Corp Data Kit labs
(Lab 4 unless noted).

---

## 4.1 From Pipelines to Agents

### Title: 4.1: Adaptive routing

**Voice over:**

Everything so far is one pipeline. A very good pipeline: hybrid
retrieval, memory, self correction, dashboards. And completely rigid:
every query gets the same treatment regardless of what it actually
needs. Chapter two already snuck a decision maker in front of the
pipeline with adaptive triggering. This chapter makes that idea the
architecture, and we climb to it in two steps: routing first, because
it is the cheapest form of agency, then the full agent loop. Look at
Example Corp's traffic and a few shapes repeat all day. Error code
lookups: what is ERR-4402. How to questions: how do I set up report
bursting. API questions: what does the refresh endpoint return.
Comparisons: Snowflake versus BigQuery connector. Each shape has an
obvious best path, so routing is just matching query to path, and you
have three implementations to choose from. Rule based: a regex spots
the ERR dash pattern and routes straight to the known issues path. It
is free, it is instant, it is trivially debuggable, and at Example Corp
it covers a startlingly large share of traffic, because customers paste
error codes. An LLM router: maximum flexibility, handles anything you
did not anticipate, and costs a model call on every single query. Or a
lightweight classifier: a small trained model, cheap and fast, sitting
between the other two in both capability and cost. Real systems layer
them: rules catch the unambiguous, the classifier handles the common
shapes, and the LLM gets only the genuinely weird. And then the
OpenSearch trick that changes the economics: cache routing decisions in
the cluster. Before invoking any router, look the query up, exact match
or semantic similarity, against an index of past routing decisions.
Support traffic is brutally repetitive: the same twenty questions
arrive dressed forty different ways, so cache hit rates run high. Put
the math on screen: five hundred tickets a day, seventy percent served
from the routing cache, and your LLM routing spend just dropped seventy
percent. Every day. Forever. That is what it looks like when the search
engine subsidizes the AI.

**Visuals:**

- Title slide: "4.1: From Pipelines to Agents."
- Rigid pipeline vs routed lanes: error code / how to / API /
  comparison, each with its best path.
- Three router cards: rules (free, narrow, debuggable) / classifier
  (cheap, common shapes) / LLM (flexible, per call cost); layered stack
  visual: rules > classifier > LLM.
- Cache flow: query > support-route-cache (exact + semantic lookup) >
  hit: route free / miss: route, then cache.
- Demo (Lab 4 Step 6): the paraphrase cache hit on screen: "steps to
  configure report bursting" hits the cached decision for "how do I set
  up report bursting" at score ~1.93, returns howto_path; an unrelated
  question scores ~1.20 and misses the threshold.
- On screen math: 500/day x 70% cache hits > routing spend down 70%.
  Caption: "the search engine subsidizes the AI."

### The ReAct loop & tool descriptions

**Voice over:**

Routing picks a lane before the work starts. An agent goes further: it
makes decisions during the work. That is the ReAct loop: reason about
what is needed, act by calling a tool, observe the result, and reason
again, repeating until it can answer or a limit says stop. Abstract
until you watch one run, so let's trace the tool on a real query.
Customer on 4.9 writes: schema discovery times out on our biggest
warehouse. Iteration one. Reason: sounds like a known failure mode,
check the known issues database before anything else. Act: search known
issues for schema discovery timeout. Observe: ERR-2288, schema
discovery timed out, affects 4.8 through 5.0, workaround is scoping the
connection to specific schemas, fixed in 5.1. Iteration two. Reason:
workaround exists and applies to 4.9, now get the customer the exact
steps. Act: search the docs for schema discovery configuration.
Observe: the schema discovery configuration pages, the scoping steps.
Now answer: acknowledge the known issue, give the scoping steps,
mention the 5.1 fix, cite both sources. Notice what just happened: no
pipeline we wrote chose that two step sequence. The agent composed it,
and a different query would compose differently. Which brings us to the
design lever that determines whether any of this works, and it is
embarrassingly unglamorous: tool descriptions. The agent chooses tools
by reading their descriptions, nothing else. A tool described as
searches docs will be used vaguely and wrongly. A tool described as
searches Example Corp known issues, returns error code, affected
versions, and workaround, prefer this for error codes and version
specific failures, gets used precisely. Write tool descriptions like
documentation for a sharp new teammate on their first day, because that
is functionally what the agent is on every single query. Two more 3.6
notes before we move on. The agent framework reports token usage per
interaction, transparent cost per loop, keep it visible, lesson 4.3
depends on it. And the V2 chat agent streamlines conversational agent
workflows, which is where the agentic memory from chapter two plugs in.

**Visuals:**

- ReAct loop diagram: Reason > Act (tool call) > Observe > repeat >
  Answer, with a stop condition slot (foreshadow 4.3).
- Demo (Lab 4 Step 4): the two iteration ERR-2288 trace, run live, each
  step labeled, final answer citing known issue + docs.
- Tool description before/after: "searches docs" vs full description
  with returns and prefer-when guidance; caption "docs for a sharp new
  teammate."
- 3.6 badges: token usage per interaction (arrow: lesson 4.3) / V2 chat
  agent + agentic memory (chapter 2 callback).

---

## 4.2 Multi-Index Agents

### Title: 4.2: Multi-Index Agents

**Voice over:**

So far the tool searches one index, and honestly, our five assets never
wanted to live together. Chapter one told us why in slow motion: they
parse differently, they chunk differently, they filter differently, and
they deserve different retrieval strategies. A known issue is a tiny
exact record. A docs page is long structured prose. A ticket is a
conversation. Cramming them into one index means one retrieval
configuration compromising for all of them. So split along the natural
seams, four indexes. Product docs and integration guides together as
support-docs, because they share structure and chunking. Resolved
tickets as support-tickets. The known issues database as
support-issues. The API reference as support-api. Now each index gets
the retrieval it actually deserves, and this is chapter one paying
dividends. Known issues: lexical first, because error codes are literal
strings and it is a small, exact set of records; hybrid overhead buys
nothing. Docs: full hybrid with parent child expansion, retrieve the
precise child, hand the model the parent section, exactly as designed
in lesson 1.3. Tickets: lean the fusion weights toward the vector leg,
because customers describe symptoms in customer words, and the best
matching ticket rarely shares vocabulary with the new one. And you do
not guess those weights: the golden set discipline from chapter one is
how you prove them. The API reference: exact matching on endpoint paths
plus semantic for the descriptions. Then each index becomes a tool,
with its own carefully written description in the style lesson 4.1
taught, and the agent selects per question. An error code question goes
to issues. A how does another customer handle this question goes to
tickets. The routing you built in 4.1 and the tool selection the agent
does here are the same skill at two altitudes.

**Visuals:**

- Title slide: "4.2: Multi-Index Agents."
- Seam diagram: five assets settling into four indexes: docs+guides /
  tickets / issues / api.
- Four index cards with strategy badges: support-issues (lexical first,
  small exact set) / support-docs (hybrid + parent child, 1.3 callback)
  / support-tickets (vector weighted fusion, customer words) /
  support-api (exact path + semantic descriptions).
- Each card framed as a tool with a one line description (4.1 style).
- Demo (Lab 4 Steps 1-3): the four indexes created and loaded by asset
  family; the issues index visibly has NO vector field; the ERR-2288
  lookup returns rank 1 instantly from 15 records.

### Cross-index synthesis, aliases & security

**Voice over:**

Some questions need several indexes at once, and our chapter three
nemesis is the perfect example. The version mismatch case truly
resolves only when the agent can combine three things: the known issue
for ERR-2209 from support-issues, the docs pages describing what the
setting actually is from support-docs, and the resolved tickets from
support-tickets, where you learn how these cases actually ended,
because knowing the humans' track record beats guessing. The agent has
two ways to gather that evidence. Sequential tool calls, one per
iteration of the ReAct loop, which is right when each result should
steer the next search. Or a meta tool: a single _msearch call that fans
one question across all four indexes in one round trip, the same
primitive you met in lesson 2.3, promoted from pipeline trick to agent
tool. Give the agent both, and say so in the descriptions: sequential
when you need to steer, _msearch when you need breadth fast. Two
operational rules make multi index agents survivable in production.
First, every tool points at index aliases, never at physical index
names. When lesson 1.4's model lifecycle forces a reindex, the alias
flips from v1 to v2 and every agent keeps working mid conversation, no
deploy, no broken tools. Second, in multi tenant deployments, enforce
document level security in the cluster itself, so a tenant scoped agent
is physically incapable of retrieving another customer's tickets, no
matter how creatively a prompt asks. An agent's instructions are
suggestions. The security layer is law, and law lives below the agent,
not inside its prompt.

**Visuals:**

- Synthesis diagram: known issue (issues) + the setting explained
  (docs) + how past cases ended (tickets) > one grounded answer.
- Two gather modes: sequential calls (steer) vs _msearch meta tool
  fanning the indexes (breadth); 2.3 callback badge.
- Demo (Lab 4 Step 5): the three-index _msearch on screen: the known
  issue, connector docs pages, resolved ERR-2209 tickets, one round
  trip.
- Alias layer: tools > aliases > physical v1/v2 indexes, flip animation
  mid conversation (1.4 callback). Demo note: Lab 4 Step 2 performs
  this exact flip live.
- Security floor: document level security under the agent; caption
  "instructions are suggestions, the security layer is law."

---

## 4.3 Guardrails & Production Concerns

### Title: 4.3: Guardrails & Production Concerns

**Voice over:**

Agents introduce a production risk no fixed pipeline ever had: a system
that decides how much work to do can decide to do far too much. Here is
the pathology. One ambiguous ticket arrives, the agent searches, is not
satisfied, reasons that it should search differently, searches again,
consults a second index, reconsiders, and fifteen tool calls and ninety
seconds later it has burned a token bill that would make finance cry,
for one ticket. At five hundred tickets a day, spirals are not an edge
case. They are a budget line and a latency incident waiting for a bad
Monday. So every agent run stays inside four ceilings, checked on every
iteration of the loop. An iteration ceiling: at most five trips around
ReAct, generous for real questions, fatal for spirals. A token ceiling
per request, enforced with the 3.6 token usage tracking you kept
visible from lesson 4.1, because you cannot enforce a budget you cannot
see. A wall clock timeout that respects the SLA math: if the answer is
not assembled in time, more searching is not the fix. And a cost
ceiling per conversation, because a forty turn escalation should not
cost more than the human it is assisting. The crucial design decision:
hitting a ceiling is not an error. The agent stops, answers from the
evidence it has already gathered, flags reduced confidence, and
escalates to a human. Sound familiar? It is exactly the graceful
degradation you built into the correction loop in chapter three, and
the consistency is the point: whether the limit is retries or
iterations or tokens, this system fails honest, never confident.

**Visuals:**

- Title slide: "4.3: Guardrails & Production Concerns."
- Spiral trace: 15 tool calls, 90 seconds, token counter spinning, one
  ambiguous ticket.
- Four ceiling cards checked per loop iteration: iterations (5) /
  tokens (3.6 tracking badge) / wall clock (SLA math) / cost per
  conversation.
- Ceiling hit path: stop > answer from gathered evidence > flag
  confidence > escalate; chapter 3 callback badge.
- Motto card: "fail honest, never confident."

### CRAG in tool wrappers & the semantic cache

**Voice over:**

Now compose the chapters, because this is where the course stops being
four separate patterns. First composition: wrap every retrieval tool
with the chapter three grader. Each tool call returns its results plus
a quality verdict, so what the agent observes is not just what came
back, but whether it is any good, and the grader's reason rides along.
Weak evidence stops being something the agent discovers three
iterations later, or worse, never. It becomes an observation the agent
reasons about immediately: this search graded poorly on version fit,
reformulate with the version filter and try the tickets index.
Corrective RAG stops being a pipeline stage and becomes a property of
every tool the agent owns. Second composition attacks cost from the
other side: a semantic cache in OpenSearch, in front of the whole
agent. Before any loop runs, embed the incoming query and search a
cache index of previously answered questions. If a semantically close
question was answered recently, for a compatible tenant tier and the
same product version, serve the cached answer in milliseconds, zero LLM
calls, zero tool calls. Example Corp sees the same renewal season
questions hundreds of times each quarter; the cache turns that repeat
traffic into index lookups. Three disciplines keep the cache honest.
Set the similarity threshold conservatively, because a near miss served
confidently is a chapter three failure wearing a performance
optimization costume. Scope cache keys by product version and tenant
tier, for exactly the reasons the version mismatch case seared into us:
a cached 5.1 answer must return nothing at all for a 4.8 customer. And
expire entries when the underlying docs change, wiring invalidation to
the update patterns from lesson 1.4: the nightly docs sync and the
known issues webhook are your cache invalidation triggers, already
built.

**Visuals:**

- Tool wrapper diagram: tool call > results + CRAG grade + reason >
  agent observes evidence and verdict together > reformulates
  immediately.
- Caption: "correction becomes a property of every tool."
- Semantic cache flow: query embedding > support-answer-cache > hit
  (ms, zero LLM calls) / miss (run agent, cache result).
- Demo (Lab 4 Step 7): the scoped cache on screen: the 5.1 customer's
  paraphrase hits and returns the cached answer; the SAME question
  scoped to 4.8 returns empty; changing the source chunk deletes
  exactly the entries built on it.
- Three discipline badges: conservative threshold ("near miss = ch3
  failure in costume") / scope by version + tier / TTL wired to 1.4
  update triggers (nightly sync, issues webhook).

### Traces, tool failures & chapter close

**Voice over:**

Two last production habits, and then the build is complete. First, log
the full execution trace of every agent run into the traces index from
lesson 3.3: every reasoning step, every tool call with its arguments,
every observation, every grade, every ceiling event, and the per
interaction token counts 3.6 hands you. When an agent misbehaves, and
one will, the trace is the difference between a five minute diagnosis
and a haunted system nobody trusts. Your dashboards grow new panels for
free: tool call distributions, iteration histograms, which tools
produce evidence that actually survives grading, where ceilings fire
most. Second, plan for tool failure, because indexes time out, models
throttle, and networks network. A failed tool call must return a
structured error the agent can reason about, not an exception that
kills the loop and not a silent retry that hides the problem. Give the
agent explicit failure guidance in the tool descriptions: if the
tickets index times out, fall back to docs and note the gap in your
answer. Degraded and honest beats crashed, and it also beats secretly
incomplete. And with that, step back and look at the whole build.
Chapter one: retrieval you can trust and measure. Chapter two: memory,
so conversations work. Chapter three: correction and evaluation, so the
system knows when it is wrong. Chapter four: agency with ceilings and
telemetry, so it can be smart without being expensive or reckless. The
build is done. And in the companion labs you run the payoff yourself:
one question, retrieved through the tuned pipeline, packed with
parent child discipline, answered by a real model with citations, and
when the customer's version does not fit the evidence, the system says
so instead of guessing. The conclusion tackles the question you should
now be asking about your own system: how much of this stack do you
actually need?

**Visuals:**

- Trace timeline: reason > tool + args > observe > grade > ceiling
  events + token counts > support-traces (3.3 callback).
- New dashboard panels: tool call distribution / iteration histogram /
  evidence survival by tool / ceiling fire rate.
- Tool failure card: structured error > agent reasons > fallback source
  + noted gap; red X on crashed loop and on silent retry.
- Full stack recap tower: Ch1 retrieval > Ch2 memory > Ch3 correction >
  Ch4 agency + guardrails = the build complete.
- Demo (Lab 4 Step 9): the capstone on screen, both runs. 5.1 customer:
  cited TLS 1.3 answer. 4.8 customer: "the fix requires 5.0; upgrade or
  contact support; no workaround exists for 4.8." Caveat chip: "your
  model's wording will differ; the honesty must not."
- Handoff: "how much do YOU need?" > conclusion.

---

## Change log vs the current draft (for review)

1. **4.1:** the comparison example became "Snowflake versus BigQuery
   connector" (matches corpus and demos; was "data warehouse versus
   analytics platform"). The ReAct trace's second act now says "search
   the docs for schema discovery configuration" (the validated demo
   searches docs; the old draft said "the data warehouse integration
   guide," which is not where the corpus keeps those steps). Routing
   cache visuals now carry the real validated scores (~1.93 hit, ~1.20
   miss).
2. **4.2:** "only a few hundred records" became "a small, exact set of
   records" (the demo index holds 15; the old phrasing would contradict
   the screen). Added one sentence tying the tickets fusion weights to
   the golden set discipline (that exact tuning is now a validated Lab
   1 step). The synthesis beat was reworded: tickets show "how these
   cases actually ended" rather than promising a pre-5.0 success story
   the corpus does not contain (same fix as chapter 3's change).
3. **4.3:** added one sentence to the cache-scoping discipline making
   the validated demo's behavior explicit (a 5.1 answer returns nothing
   for a 4.8 customer). The chapter close now includes the capstone
   demo beat (real end-to-end RAG answer with citations and an honest
   version refusal), which is the emotional payoff of the whole build
   and is validated in Lab 4 Step 9.
4. **3.6 features note (applies to 4.1 and 4.3):** token usage
   tracking, V2 chat agent, and agentic memory are narrated as 3.6
   features and were NOT validated (demo cluster is 3.5). Keep the VO
   as is only if recording after a 3.6 validation pass, or soften to
   "the newest OpenSearch versions" if recording before it.
5. **Demo callouts** throughout now point at specific Lab 4 steps with
   validated outputs.
