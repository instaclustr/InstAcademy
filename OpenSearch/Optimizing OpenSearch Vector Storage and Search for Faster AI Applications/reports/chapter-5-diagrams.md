# Chapter 5 diagram recommendations

This report identifies eight places in the Chapter 5 README where a diagram or chart would resolve a spatial or numeric relationship that students currently must hold in their heads.

## 1. The over-sharded index: 24 shard copies chasing 18 slots

**Placement:** Lesson 5-1, Step 1, after the paragraph that begins "Why exactly 6 unassigned_shards?" (the paragraph directly below the cluster health JSON response).

**Type:** Architecture diagram (labeled node-and-shard layout).

**Why:** Students must mentally multiply 6 shards by 4 copies, distribute them across 3 nodes under the "no node holds two copies of the same shard" rule, and arrive at exactly 6 leftovers, which is far easier to see than to compute.

**Creation prompt:** Create an architecture diagram that explains why an OpenSearch index with 6 primary shards and 3 replicas per shard leaves exactly 6 shard copies unassigned on a 3-node cluster. Title at the top: "6 shards × 4 copies = 24 copies, but 3 nodes only offer 18 legal slots". Layout: three large rounded rectangles side by side across the middle, labeled "Data node A", "Data node B", and "Data node C". Inside each node, draw six small shard chips arranged in a 2×3 grid. Node A contains chips labeled P0, P1, R2, R3, R4, R5. Node B contains P2, P3, R0, R1, R4, R5. Node C contains P4, P5, R0, R1, R2, R3. Color primary chips (P0 to P5) in a solid blue and replica chips (R) in a lighter blue. Below the three nodes, draw a gray dashed rectangle labeled "Unassigned (nowhere legal to go)" containing six gray chips labeled R0, R1, R2, R3, R4, R5. Add a callout box pointing at the nodes that reads: "Rule: a node never holds two copies of the same shard". Add a math strip along the bottom: "6 primaries + (6 shards × 3 replicas) = 24 copies. 3 nodes × 6 shards each = 18 slots. 24 - 18 = 6 unassigned". In the top right corner, place a status badge: a yellow circle with the text "Cluster status: YELLOW, unassigned_shards: 6". Add a small footnote under the badge: "Fix: set number_of_replicas lower, and the cluster goes GREEN in seconds". Style: clean flat technical illustration for a video course slide, white background, limited color palette (blues and grays with one accent color), large readable labels, no logos, no watermark.

## 2. Disk watermark thresholds at 85, 90, and 95 percent

**Placement:** Lesson 5-1, Step 3, after the opening paragraph that begins "You fixed this incident because you caused it" (the paragraph that says unassigned shards in production are very often a disk problem in disguise), before the first `_cat/allocation` request.

**Type:** Labeled illustration (horizontal gauge).

**Why:** The chapter says disk problems cause most real allocation failures, and a gauge makes the three default watermark thresholds and their escalating consequences visible at a glance.

**Creation prompt:** Create a horizontal gauge illustration of the three default OpenSearch disk watermark thresholds on a single data node. Title at the top: "Disk watermarks: what happens as a data node fills up". Draw one wide horizontal bar spanning the slide, representing disk usage from 0% on the left to 100% on the right, with tick marks at 0, 25, 50, 75, and 100. Divide the bar into four colored zones: 0% to 85% in a calm blue-gray labeled "Normal: shards allocate freely", 85% to 90% in light amber labeled "Low watermark (85%)", 90% to 95% in darker amber labeled "High watermark (90%)", and 95% to 100% in red labeled "Flood stage (95%)". Above the bar, add three callout boxes with arrows pointing to the 85, 90, and 95 marks. The 85% callout reads: "Node stops accepting NEW shards". The 90% callout reads: "Cluster actively moves shards OFF this node". The 95% callout reads: "Indexes with a shard here become read-only". Below the bar, add a small marker with an arrow at roughly the 1% position labeled "This course's demo cluster: 1% used, 28.7 GB free". Add a footnote line at the bottom: "These are the OpenSearch defaults; check them with GET _cat/allocation". Style: clean flat technical illustration for a video course slide, white background, limited color palette (blues and grays with one accent color), large readable labels, no logos, no watermark.

## 3. The shrink recipe: eight steps to fewer shards

**Placement:** Lesson 5-2, before Step 4, after the lesson introduction paragraph that ends "if you sized it wrong."

**Type:** Flowchart.

**Why:** The shrink recipe is read-along reference material with no hands-on steps, so a single flowchart is the only place students will see the strict ordering of its eight operations.

**Creation prompt:** Create a flowchart of the OpenSearch shrink recipe, which reduces the shard count of an existing index. Title at the top: "The shrink recipe: from 6 shards to 2, safely". Layout: eight numbered boxes connected by arrows, arranged in two rows of four, flowing left to right on the top row, then dropping down and flowing left to right again on the bottom row. Box 1: "Block writes on the source index (index.blocks.write: true)". Box 2: "Pin one copy of every shard onto a single node (routing allocation setting)". Box 3: "POST _shrink to create the target index with fewer shards". Box 4: "Clear the routing pin on the new index". Box 5: "Force merge the new index (max_num_segments: 1)". Box 6: "Create an alias pointing at the new index". Box 7: "Swap the alias so applications cut over with zero downtime". Box 8: "Delete the source index". Color boxes 1 and 2 in gray (preparation), boxes 3, 4, and 5 in blue (the shrink itself), and boxes 6, 7, and 8 in a green accent (cutover and cleanup). Add a small legend for the three colors: "Prepare", "Shrink", "Cut over". Add one callout note attached to box 3 that reads: "Target shard count must divide evenly into the source count: 6 → 3, 2, or 1". Style: clean flat technical illustration for a video course slide, white background, limited color palette (blues and grays with one accent color), large readable labels, no logos, no watermark.

## 4. The write alias, rollover, and ISM lifecycle

**Placement:** Lesson 5-2, Step 6, after the step's opening paragraph that begins "Data like logs, metrics, and search history never stops arriving", before the first ISM policy request.

**Type:** Flow diagram with a before/after pair.

**Why:** Students must track four moving parts at once (the application, the alias, two physical indexes, and the ISM policy), and a before/after picture shows the alias moving while the application never changes what it writes to.

**Creation prompt:** Create a two-panel before-and-after flow diagram of an OpenSearch write-alias rollover managed by an ISM policy. Title at the top: "Rollover: the alias moves, the application never notices". Left panel, labeled "Before rollover": a box on the left labeled "Application" with an arrow labeled "writes" pointing to a diamond-shaped badge labeled "alias: searches-current", which points with a solid arrow to a rectangle labeled "searches-000001, is_write_index: true, 6 docs". Right panel, labeled "After rollover": the same "Application" box and the same "searches-current" alias badge, but the alias now has two arrows: a solid arrow labeled "writes" to a new rectangle "searches-000002, is_write_index: true", and a dashed arrow labeled "still searchable" to the old rectangle "searches-000001, is_write_index: false". Between the panels, place a bold arrow labeled "_rollover fires: 6 docs ≥ min_doc_count 5". Across the top, draw one wide box labeled "ISM policy: bookstore-searches-policy" containing two mini states connected by an arrow: "hot: roll over at 5 docs" then "delete: remove index after 90 days". From this policy box, draw a thin dashed arrow down to the indexes labeled "checks every ~5 minutes, attaches to any new searches-* index automatically". Use blue for the active write index in each panel, light gray for the retired index, and one accent color for the alias badge. Style: clean flat technical illustration for a video course slide, white background, limited color palette (blues and grays with one accent color), large readable labels, no logos, no watermark.

## 5. Vector memory math: from one vector to 10 million books

**Placement:** Lesson 5-3, after the lesson introduction paragraph that begins "Vectors are memory hogs by design", before Step 7.

**Type:** Labeled illustration (three-stage scaling diagram).

**Why:** The intro compresses four multiplications into two sentences, and a scaling picture lets students see how 3,072 bytes per vector becomes a 45 GB problem.

**Creation prompt:** Create a three-stage scaling illustration showing how vector memory grows in an OpenSearch bookstore index. Title at the top: "Why vectors are memory hogs: the bookstore math". Layout: three groups arranged left to right, connected by arrows labeled "× 500,000 books" between group 1 and group 2, and "× 20 (10M books)" between group 2 and group 3. Group 1, labeled "One embedding": a small strip of squares suggesting a vector, captioned "768 dimensions × 4 bytes (float32) = 3,072 bytes". Group 2, labeled "500k books": a medium stacked box with two segments, a blue segment captioned "raw vectors ≈ 1.5 GB" and a lighter blue segment on top captioned "+ ~50% HNSW graph overhead ≈ 2.25 GB total", with a green check mark note "fits comfortably in one shard's RAM". Group 3, labeled "10M books": a much taller stacked box captioned "≈ 45 GB", with a warning note "does not fit one node, must spread across shards and nodes". Draw the three boxes with visibly increasing heights so the scale jump is obvious, but do not attempt exact proportional scale; add a small note "box heights not to scale". At the bottom, add a strip labeled "Two escape hatches when RAM is the constraint" containing two pills: "on_disk mode" and "fp16 scalar quantization (Step 7)". Style: clean flat technical illustration for a video course slide, white background, limited color palette (blues and grays with one accent color), large readable labels, no logos, no watermark.

## 6. What lives on disk versus what loads into RAM

**Placement:** Lesson 5-3, Step 8, after the paragraph that begins "Same 50 documents, but fp16 is only about 24% smaller on disk" (the paragraph explaining why disk did not halve).

**Type:** Labeled illustration (two-column anatomy diagram).

**Why:** The counterintuitive result that fp16 halves memory but only trims disk by 24% becomes obvious once students see that the full-precision vector file stays identical and only the graph file loads into RAM.

**Creation prompt:** Create a two-column anatomy diagram comparing what an OpenSearch float vector index and an fp16 quantized index store on disk versus what they load into RAM. Title at the top: "Quantization buys memory, not disk". Two columns side by side: left column headed "book-embeddings-float (32-bit)", right column headed "book-embeddings-fp16 (16-bit, sq encoder)". Both columns note "same 50 vectors, 768 dims". Each column has two horizontal layers. The upper layer is labeled "DISK" and contains two file boxes: a gray box labeled "Full-precision vectors (Lucene .vec file): 153,708 bytes" drawn at identical width in both columns, and a blue box labeled "FAISS HNSW graph file" drawn at full width in the float column and at roughly half that width in the fp16 column. Under each DISK layer, print the total: "Total on disk: 321,626 bytes" for float and "Total on disk: 244,886 bytes (only 24% smaller)" for fp16. The lower layer is labeled "RAM (loaded for search)" and contains only one box per column: "graph in memory: 157 KB per shard copy" for float and "graph in memory: 82 KB per shard copy (48% less)" for fp16. Draw an arrow from each blue graph file box down into the RAM layer labeled "only the graph loads into memory". Draw a crossed-out arrow from the gray .vec box toward RAM labeled "never loaded for HNSW search". Bottom takeaway strip: "The full-precision copy stays on disk untouched. Quantization halves the graph, and the graph is what fills your RAM." Style: clean flat technical illustration for a video course slide, white background, limited color palette (blues and grays with one accent color), large readable labels, no logos, no watermark.

## 7. Float versus fp16: the measured results

**Placement:** Lesson 5-3, Step 8, after the closing paragraph that begins "There is the proof" (end of the step, before the Fast mode line).

**Type:** Grouped bar chart, two panels.

**Why:** The step's four measured numbers arrive across three separate API responses, and one chart puts the whole experiment's result on a single slide for the video.

**Creation prompt:** Create a two-panel bar chart comparing a float32 vector index against an fp16 quantized index in OpenSearch, using real measured values from identical data (50 vectors, 768 dimensions, only difference is the fp16 sq encoder). Title at the top: "fp16 versus float32: measured on the course cluster". Left panel titled "Disk store size (primary shard, bytes)": two vertical bars, "float32" at 321,626 and "fp16" at 244,886, with the exact values printed above each bar and a bracket annotation between them reading "24% smaller". Right panel titled "HNSW graph memory after warmup (KB per shard copy)": two vertical bars, "float32" at 157 and "fp16" at 82, values printed above each bar, bracket annotation reading "48% less, this is the RAM that matters". In both panels, color the float32 bar gray and the fp16 bar blue, and start the y-axis at zero. Add a footnote under the left panel: "Disk shrinks less because both indexes keep an identical 153,708-byte full-precision vector file". Add a footnote under the right panel: "Cluster total: two copies each (primary + replica), so 157+157 KB versus 82+82 KB". Style: clean flat technical illustration for a video course slide, white background, limited color palette (blues and grays with one accent color), large readable labels, no logos, no watermark.

## 8. The shard request cache: miss, hit, and invalidation

**Placement:** Lesson 5-4, Step 9, after the paragraph that begins "One miss and one hit" (the paragraph explaining the cache counters), before the Fast mode line.

**Type:** Flowchart.

**Why:** The step spreads the miss path, the hit path, and the automatic invalidation guarantee across three requests, and a single flow shows why the second identical query cost 0 milliseconds and why stale results are impossible.

**Creation prompt:** Create a flowchart of the OpenSearch shard request cache handling the same query twice. Title at the top: "Shard request cache: first run computes, second run remembers". Layout top to bottom. Start box: "Search arrives: GET my-index/_search?request_cache=true with size: 0 (counts and aggregations only, the cacheable kind)". Arrow down to a decision diamond: "Result already in the shard request cache?". Two branches. Left branch labeled "No (run 1)": box "Execute the query on the shard, took: 2 ms", then box "Store the 689-byte result in the cache, miss_count: 1". Right branch labeled "Yes (run 2)": box "Serve straight from memory, took: 0 ms, hit_count: 1", drawn in the accent color to mark the win. Both branches point down to a shared result box: "Identical response either way: hits.total.value: 10, empty hits array". To the side, add a separate gray box labeled "Safety valve" containing: "New data indexed → shard refresh → cached entries invalidated automatically, so the cache never serves stale results", with a dashed arrow from it to the cache diamond. Bottom strip showing the counters as three small tiles: "hit_count: 1", "miss_count: 1", "memory_size_in_bytes: 689". Style: clean flat technical illustration for a video course slide, white background, limited color palette (blues and grays with one accent color), large readable labels, no logos, no watermark.
