# Chapter 1 exam guide

**Optional** — study questions for Chapter 1. Not required for the hands-on labs.

← [Chapter 1](../src/Chapter%201/README.md) · [Course index](../README.md)

# Chapter 1 Exam Guide — Indexing and Optimizing for Vector Search with OpenSearch

---

## Questions

### Question 1 (Chapter 1, Lesson 1: Vector Search Settings)

Your bookstore wants to add semantic search to its product catalog. A team member suggests storing book descriptions as-is and running keyword searches. Why would you use vector embeddings instead?

A) Vector embeddings compress text to save disk space, so you can store more books per node.

B) Vector embeddings are numerical representations of data created by ML models that capture semantic meaning, enabling searches to find results based on context rather than exact keyword matches.

C) Vector embeddings replace the need for an OpenSearch cluster entirely, since all search happens inside the ML model.

---

### Question 2 (Chapter 1, Lesson 1: Vector Search Settings)

Your bookstore has a large catalog of older, rarely updated books. You want to reduce memory costs for storing their embeddings. Which optimization technique stores vectors primarily on disk and uses quantization to dramatically lower memory usage?

A) Memory-optimized search, which uses the OS file system to memory-map the index and page data in and out as needed.

B) Disk-based search optimization, which uses binary quantization (with optional scalar quantization) to compress vectors, keeping only a small compressed index in memory while storing full-precision vectors on disk.

C) Segment merging, which consolidates Lucene segments to reduce the number of files per shard.

---

### Question 3 (Chapter 1, Lesson 2: Choosing the Right Type of Vector Search)

Your bookstore has a small, curated collection of 5,000 rare first-edition books. Customers need perfect accuracy when searching — every relevant result must appear. Which vector search algorithm should you use?

A) HNSW (Hierarchical Navigable Small World), because its tiered graph structure handles large datasets efficiently.

B) IVF (Inverted File Index), because its centroid-based clustering is ideal for memory-constrained environments.

C) Exact k-NN (k-Nearest-Neighbor), because it calculates the distance between the query and every data point, delivering perfect recall on a small dataset where the computational cost is acceptable.

---

### Question 4 (Chapter 1, Lesson 1-3: GPUs vs CPUs in OpenSearch)

Your bookstore is launching a new e-commerce search feature and needs to index 50 million product vectors. Using CPU-only indexing, this would take 2–3 days. What would GPU acceleration primarily help with in this scenario?

A) Running search queries faster, since GPUs handle all search operations in OpenSearch.

B) Dramatically speeding up the index-building process (especially HNSW graph construction), potentially reducing build time from days to hours.

C) Reducing the memory footprint of stored vectors by compressing them using GPU parallel processing.

---

### Question 5 (Chapter 1, Lesson 4: Vector Storage and Search Optimizations)

Your bookstore has thousands of lengthy knowledge-base articles for its AI support assistant. Without any preprocessing, the assistant frequently misses key troubleshooting steps. What optimization technique would fix this?

A) Dimension reduction — lowering the vector dimensions so the model processes data faster.

B) Document chunking — splitting large documents into smaller pieces before embedding, so each piece fits within the model's token limits and produces accurate embeddings.

C) Shard rebalancing — distributing the articles across more shards for parallel processing.

---

## Answer Key

### Question 1: B

A is wrong because vector embeddings increase storage requirements compared to raw text — they add high-dimensional numerical data alongside your text. C is wrong because embeddings are stored in and searched through OpenSearch; the ML model generates them, but OpenSearch handles storage and retrieval. **B is correct** because vector embeddings translate non-numeric data (like book descriptions) into numerical representations that can be reasoned about semantically, enabling searches like "cozy rainy day read" to match a book described as "a warm story set during a storm."

### Question 2: B

A describes memory-optimized search (using OS-level memory mapping / paging), which can reduce RAM usage by loading vector data on demand but does not apply aggressive quantization for massive compression.

C describes general segment management, which helps with overall index health and query latency by reducing the number of small files, but it has no direct effect on how vectors are stored or compressed.

B is correct because disk-based vector search (introduced in OpenSearch 2.17) is specifically designed for this scenario. You enable it by setting "mode": "on_disk" on the knn_vector field. This feature uses binary quantization by default (with up to 32x compression) to keep a tiny compressed version of the vectors in memory, while the full-precision vectors stay on disk. During search, it quickly finds candidate results with the compressed vectors and then rescoring with the full-precision vectors loaded from disk. This approach significantly reduces memory and operational costs for large, infrequently changing datasets, at the acceptable trade-off of slightly higher search latency and a small reduction in recall (which rescoring helps mitigate).

This optimization is ideal for older book catalogs that don’t change often and where keeping every vector fully in RAM would be expensive.

### Question 3: C

A is a strong choice for larger datasets where you need low latency and can afford more memory, but it's approximate — it may miss some relevant results, which violates the "perfect accuracy" requirement. B is best for very large datasets where memory is constrained, and it requires a training step — overkill for 5,000 books. **C is correct** because exact k-NN computes the distance to every vector in the index, guaranteeing perfect recall. On a small dataset of 5,000 books, the computational cost of this brute-force approach is acceptable.

### Question 4: B

A is wrong because search queries still run on CPU in OpenSearch — GPU acceleration currently targets the indexing process, not query execution. C is wrong because GPU acceleration doesn't compress vectors; it speeds up the mathematical operations needed to build index structures like HNSW graphs. **B is correct** because GPU acceleration's primary benefit in OpenSearch is dramatically speeding up index building, especially HNSW graph construction, where the massive parallel processing power of GPUs can reduce build time from days to hours.

### Question 5: B

A would reduce storage and improve speed, but it doesn't solve the problem of the model truncating long documents. C distributes data for parallelism but doesn't address the fact that individual documents exceed the model's token limits. **B is correct** because models have strict token limits (typically 512 tokens), and without chunking, longer articles get silently truncated — causing the assistant to miss important content. Chunking ensures every piece of text fits the model, producing more accurate embeddings and better search results.
