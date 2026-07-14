# Chapter 2 diagram recommendations

This report lists eight places in the Chapter 2 README where a diagram or chart would genuinely help students, with a paste-ready image prompt for each one.

## 1. ML Commons model lifecycle state diagram

**Placement:** Lesson 2-1, before Step 1. Insert it right after the lesson intro paragraph that explains "you register a model, deploy it, and then any ingest pipeline or query can call it."

**Type:** State diagram (flowchart of lifecycle states).

**Why:** Students must hold five lifecycle stages in their head across five steps and the cleanup section, and this diagram shows the whole journey at once, including the disk versus memory distinction that explains why deploy exists at all.

**Creation prompt:** Create a horizontal state diagram showing the OpenSearch ML Commons model lifecycle. Draw five rounded rectangle states left to right, connected by right-pointing arrows: "REGISTERED", "DEPLOYED", "UNDEPLOYED", then a final state drawn as a dashed rounded rectangle labeled "DELETED". Before the first state, add a small circle labeled "Start" with an arrow into "REGISTERED"; label that arrow "POST _register (downloads artifact)". Label the arrow from "REGISTERED" to "DEPLOYED" as "POST _deploy (loads weights into memory)". Label the arrow from "DEPLOYED" to "UNDEPLOYED" as "POST _undeploy (frees node memory)". Label the arrow from "UNDEPLOYED" to "DELETED" as "DELETE model (only allowed after undeploy)". Under the "REGISTERED" state add a caption "Artifact stored on disk". Under the "DEPLOYED" state add a caption "Weights live in node memory; serves _predict, ingest pipelines, neural queries" and highlight this state with the accent color because it is the working state. Above the diagram, add a loop-back annotation on "DEPLOYED": a curved arrow from "DEPLOYED" back to itself labeled "infer (_predict)". Add a title at the top: "ML Commons model lifecycle: register, deploy, infer, undeploy, delete". Keep all text large and the flow strictly left to right. Style: clean flat technical illustration for a video course slide, white background, limited color palette (blues and grays with one accent color), large readable labels, no logos, no watermark.

## 2. Register and deploy sequence diagram with task polling

**Placement:** Lesson 2-1, Step 3, right after the opening paragraph that says registration runs asynchronously and returns a `task_id`. It also covers Step 4, so mention it again briefly there.

**Type:** Sequence diagram.

**Why:** Students routinely confuse the two async calls, the two different task ids, and the single model id, and a sequence diagram makes the poll-until-COMPLETED pattern obvious.

**Creation prompt:** Create a sequence diagram with two vertical lifelines: "You (Dev Tools client)" on the left and "OpenSearch ML Commons" on the right. Show this exchange top to bottom as horizontal arrows between the lifelines. Arrow 1, left to right: "POST _plugins/_ml/models/_register (model name msmarco-distilbert-base-tas-b, version 1.0.3, TORCH_SCRIPT)". Arrow 2, right to left, dashed: "returns task_id (register task)". Then draw a loop box around the next two arrows labeled "Poll every few minutes (takes 2 to 3 minutes)": Arrow 3, left to right: "GET _plugins/_ml/tasks/{task_id}"; Arrow 4, right to left, dashed: "state: CREATED or RUNNING". After the loop box, Arrow 5, right to left, dashed and highlighted with the accent color: "state: COMPLETED, returns model_id (save this!)". Then Arrow 6, left to right: "POST _plugins/_ml/models/{model_id}/_deploy". Arrow 7, right to left, dashed: "returns a NEW task_id (deploy task)". Draw a second smaller loop box labeled "Poll again": Arrow 8, left to right: "GET _plugins/_ml/tasks/{task_id}"; Arrow 9, right to left, dashed: "state: COMPLETED, model is DEPLOYED on worker nodes". Finish with Arrow 10, left to right: "POST _plugins/_ml/_predict/text_embedding/{model_id}" and Arrow 11, right to left, dashed: "768-float sentence_embedding per input". Add a side note near arrows 2 and 7 reading "Two different task ids, one model_id". Title at the top: "Register, poll, deploy, poll, predict". Style: clean flat technical illustration for a video course slide, white background, limited color palette (blues and grays with one accent color), large readable labels, no logos, no watermark.

## 3. Ingest pipeline embedding at index time

**Placement:** Lesson 2-2, in the lesson intro, right after the paragraph that begins "Attach that pipeline to an index as its default_pipeline" and before the IMPORTANT note about creation order.

**Type:** Architecture flow diagram.

**Why:** This is the chapter's core invisible mechanism, and students need to see that the client sends plain text while the pipeline and model add the vector before storage.

**Creation prompt:** Create a left-to-right architecture flow diagram showing how OpenSearch embeds documents automatically at index time. Node 1 (far left): a document card labeled "Client sends plain JSON" showing two fields: "title: Frankenstein" and "passage_text: 'Frankenstein by Mary Shelley is a...'" with a caption underneath reading "No vector in the payload". Arrow right labeled "index into vector-search-index". Node 2: a tall rounded container labeled "vector-search-index setting: default_pipeline" with an arrow passing into Node 3. Node 3: a box labeled "Ingest pipeline: vector-search-embeddings-pipeline" containing one inner box labeled "text_embedding processor, field_map: passage_text to passage_embedding". From Node 3, draw an arrow down to Node 4, a box below the pipeline labeled "Deployed model: msmarco-distilbert-base-tas-b (768-dim)", with the arrow labeled "sends passage_text" and a return arrow labeled "returns 768-float vector". From Node 3 an arrow continues right to Node 5 (far right): a document card labeled "Stored document" showing three fields: "title: Frankenstein", "passage_text: 'Frankenstein by Mary Shelley is a...'", and "passage_embedding: [0.27, -0.05, -0.26, ... 768 floats]" with the passage_embedding line highlighted in the accent color. Add a caption under Node 5: "Same document, now with its embedding attached". Title at the top: "The ingest pipeline embeds every document as it arrives". Style: clean flat technical illustration for a video course slide, white background, limited color palette (blues and grays with one accent color), large readable labels, no logos, no watermark.

## 4. Neural query flow with the enricher and the shared model

**Placement:** Lesson 2-2, Step 11, right after the intro paragraph ("This is the moment the chapter promised...") and before the request block. It also reinforces Step 10, so reference it there in one sentence.

**Type:** Flow diagram with two parallel lanes.

**Why:** The key insight is that the query text and the documents pass through the same model into the same vector space, and one picture of both paths meeting at the ANN search prevents the most common mental gap in neural search.

**Creation prompt:** Create a two-lane left-to-right flow diagram showing that indexing and querying use the same embedding model. Top lane, labeled "Index time (already done)": Node A "256 book summaries (plain text)", arrow to Node B "Embedding model msmarco-distilbert-base-tas-b", arrow to Node C "256 stored vectors, 768-dim each, in vector-search-index". Bottom lane, labeled "Query time (now)": Node D "Query text: 'an ambitious scientist who comes to regret his own creation'", arrow to Node E "Search pipeline default-model-pipeline: neural_query_enricher injects default_model_id (no model_id in the query body)", arrow to Node F which is the SAME model box as Node B, so draw one shared central box labeled "Embedding model msmarco-distilbert-base-tas-b" that both lanes pass through, with a bold accent-colored callout on it reading "Same model on both paths = same vector space". From the model, the bottom lane continues with an arrow to Node G "768-dim query vector", then an arrow to Node H "HNSW ANN search, k=10, compares query vector to stored vectors". Final node on the right: Node I, a small ranked result list titled "Top hits by meaning" with the first visible entry "Frankenstein; or, the Modern Prometheus" highlighted in the accent color and a caption "Top 5 of 256 books, no title words in the query, scores cluster around 0.017 to 0.018". Title at the top: "Neural query flow: your sentence and the books meet in the same vector space". Style: clean flat technical illustration for a video course slide, white background, limited color palette (blues and grays with one accent color), large readable labels, no logos, no watermark.

## 5. Dense versus sparse embedding shapes

**Placement:** Lesson 2-3, right after the dense versus sparse comparison table and the sparse token-weight JSON example, before the "Decision framework" heading.

**Type:** Labeled side-by-side illustration.

**Why:** The dense versus sparse difference is a difference of shape, and a visual of a fully filled vector next to a mostly empty token-weight map lands faster than the table alone.

**Creation prompt:** Create a side-by-side comparison illustration of dense and sparse text embeddings, split into a left panel and a right panel of equal width. Left panel title: "Dense embedding (text_embedding processor)". Show a long horizontal strip of many small contiguous cells (draw about 24 cells and add an ellipsis) where EVERY cell is filled with color, with the first cells showing real values: 0.273, -0.051, -0.257, 0.171, 0.064, 0.132, then "...". Caption below the strip: "768 dimensions, every position has a value". Bullet labels under the left panel: "Captures deep semantic meaning and paraphrase", "Best for semantic search, recommendations, RAG", "Heavier compute at ingest and query". Right panel title: "Sparse embedding (sparse_encoding processor)". Show a similar strip of many small cells where almost all cells are empty gray outlines and only three or four cells are filled with the accent color; above each filled cell, connect a small label bubble: "today: 1.42", "sunny: 1.31", "weather: 0.44". Caption below the strip: "Tens of thousands of possible dimensions, almost all zero; only meaningful terms carry weight". Bullet labels under the right panel: "Lexical precision plus some semantics", "Best for massive datasets, low latency, hybrid search", "Lighter, cheaper to store, scales horizontally". Between the panels, place the shared input text at the top center: "Input text: 'today is sunny'" with one arrow going to each panel. Title at the top: "Two embedding shapes for the same text". Style: clean flat technical illustration for a video course slide, white background, limited color palette (blues and grays with one accent color), large readable labels, no logos, no watermark.

## 6. Chunked model storage and deployment onto worker nodes

**Placement:** Lesson 2-4, Step 13, right after the first Expected JSON block (the model metadata response that shows `total_chunks: 27`), before the Profile API request.

**Type:** Architecture diagram.

**Why:** The metadata response mentions 27 chunks and 3 worker nodes with no explanation, and this diagram shows how one 266 MB artifact becomes chunks on disk and then a live model in memory on every data node.

**Creation prompt:** Create a left-to-right architecture diagram showing how OpenSearch ML Commons stores and deploys a model. Stage 1 (left): a single large file icon labeled "Model artifact: msmarco-distilbert-base-tas-b, 266,357,253 bytes (about 266 MB), TorchScript". Arrow right labeled "register: split and store". Stage 2 (middle): a database cylinder labeled "ML model index (on disk)" containing a stack of small numbered blocks labeled "chunk 1, chunk 2, chunk 3 ... chunk 27" with a caption "total_chunks: 27, each chunk is a document in the index". Arrow right labeled "deploy: reassemble and load into memory". Stage 3 (right): three identical server boxes stacked vertically, each labeled "Data node (worker node)" and each containing a small accent-colored brain-chip icon labeled "Model in memory, about 320 MB". A brace or caption groups the three servers with the text "current_worker_node_count: 3, deploy_to_all_nodes: true". Below the three servers add one line: "Ingest pipelines and neural queries call whichever node is local, so inference stays low latency". Title at the top: "One artifact, 27 stored chunks, 3 nodes serving inference". Style: clean flat technical illustration for a video course slide, white background, limited color palette (blues and grays with one accent color), large readable labels, no logos, no watermark.

## 7. Node memory layout and the k-NN circuit breaker

**Placement:** Lesson 2-5, Step 14, right after the intro paragraph ("Here's a fact that surprises most people...") and before the request block.

**Type:** Labeled illustration (stacked memory bar).

**Why:** The whole point of the step is that HNSW graphs live outside the JVM heap, and a single memory-bar picture makes the invisible native region and the 50% guardrail concrete.

**Creation prompt:** Create a labeled illustration of RAM usage on a single OpenSearch data node, drawn as one wide horizontal bar divided into segments, with callout labels above and below. The full bar is titled "Total node RAM". Left segment (about 40% of the bar, medium blue): "JVM heap: index buffers, query caches, aggregations" with a callout above reading "This is what your heap dashboards monitor". Right segment (the remaining 60%, light gray) labeled "Native memory (outside the JVM heap)". Inside the native segment, shade the left half in the accent color and label it "k-NN graph memory: HNSW graphs live HERE", and mark the boundary in the middle of the native segment with a bold vertical dashed line labeled "knn.memory.circuit_breaker.limit: 50% of memory left after the heap". Add a callout below the accent area reading "At the limit, least recently used graphs are evicted instead of the node running out of memory". Add a warning callout above the native segment: "A vector index can exhaust node RAM while every heap dashboard still shows green". Title at the top: "Where HNSW graphs actually live, and the guardrail that protects the node". Style: clean flat technical illustration for a video course slide, white background, limited color palette (blues and grays with one accent color), large readable labels, no logos, no watermark.

## 8. Filter before vectors funnel

**Placement:** Lesson 2-5, Step 16, right after the two explanation paragraphs under "The Search Query Below..." and before the request block.

**Type:** Funnel flowchart.

**Why:** Students need to see that the cheap yes/no filter shrinks the candidate set before any vector math runs, which is the shape change that makes filtered neural search fast at scale.

**Creation prompt:** Create a top-to-bottom funnel flowchart showing metadata filtering before vector search in OpenSearch. Level 1 (top, widest): a wide band of many small book icons labeled "Full corpus: 256 books in vector-search-index". Arrow down through a gate-shaped bar labeled "Step 1: filter runs first. term: bookshelves = 'Category: Romance'. Cheap yes/no check, no scoring, no ranking". Level 2 (middle, much narrower): a smaller band of book icons in the accent color labeled "Eligible set: only romance-shelved books". Arrow down through a second bar labeled "Step 2: neural search runs on this subset only. query_text 'a tragic romance' becomes a 768-dim vector, HNSW finds k=10 nearest neighbors". Level 3 (bottom): a ranked list card titled "Top 10 results" with visible entries: "1. Romeo and Juliet", "2. Romeo and Juliet (second Gutenberg edition)", "3. Carmen", "4. Manon Lescaut", and a grayed lower entry "A Midsummer Night's Dream (comedy, ranks lower)". To the right of the funnel, add a vertical annotation with an arrow spanning levels 1 to 2 reading "Excluded early: philosophy texts and sea adventures never get scored". Add a bottom caption: "On 256 books the speedup is invisible; on millions of documents this is the difference between a fast query and a slow one". Title at the top: "Filter first, then rank: ANN only scores books that could qualify". Style: clean flat technical illustration for a video course slide, white background, limited color palette (blues and grays with one accent color), large readable labels, no logos, no watermark.
