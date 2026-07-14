← [Course index](README.md) · [How to run labs](HANDS-ON-GUIDE.md) · [Cluster setup](CLUSTER-SETUP.md)

# Changelog

All notable changes to this course are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the course uses [semantic versioning](https://semver.org/) adapted for learning material:

- **Major** (2.0.0): a restructure that changes the chapter or lesson lineup, so anyone mid-course would need to restart.
- **Minor** (1.1.0): steps added, removed, or renumbered inside a chapter, or a new OpenSearch version validated.
- **Patch** (1.0.1): corrections, clearer wording, updated screenshots, no change to what you run.

## [1.0.0] — 2026-07-14

First release of the course as a complete, end-to-end validated workshop. Every hands-on step in all five chapters was executed against a live OpenSearch 3.5.0 cluster, and the **Expected** output shown in each step is the real response from that run.

### Added
- Five chapter workshops with **72 hands-on steps** (Chapter 1: 16, Chapter 2: 16, Chapter 3: 14, Chapter 4: 15, Chapter 5: 11).
- Chapter 4 Step 15: connect **Claude Desktop** to the cluster over the built-in MCP server, including [`src/Chapter 4/mcp-basic-auth-bridge.mjs`](src/Chapter%204/mcp-basic-auth-bridge.mjs), a zero-dependency stdio-to-HTTP bridge written for this course because `mcp-remote` cannot authenticate against a basic-auth MCP endpoint.
- 40 diagrams (8 per chapter) illustrating the concepts behind each lesson.
- Bruno "fast mode" collection mirroring every request in every chapter.
- [`CLUSTER-SETUP.md`](CLUSTER-SETUP.md): sign-up, cluster creation, firewall rules, connection details, and a health check.

### Changed
- Every bulk payload is inlined in its chapter README, which is now the single source of truth. The files in `rest/bulk/` are the machine-readable mirror that the Bruno collection sends.

### Known limitations
- **OpenSearch 3.5.0 quirks** documented inline where they bite: `profile: true` breaks on `hybrid` queries; `filter_query` and `normalization-processor` do not compose in one search pipeline; the Faiss `sq` encoder takes no `bits` parameter; `_rank_eval` accepts no `search_pipeline` parameter; the MCP `tools/_remove` body is a bare JSON array that the Dev Tools console cannot send.
- **Managed-cluster network policy**: outbound calls from the cluster reach `api.cohere.ai` but not `api.openai.com` or `api.anthropic.com`, so server-side LLM connectors are out of scope for this course.
- The built-in MCP server is an experimental ML Commons feature (it self-reports version 0.1.0) and is not an officially supported Instaclustr feature. It works on OpenSearch 3.3 and later.

## Compatibility

| Course version | Validated on | Cluster |
|---|---|---|
| 1.0.0 | OpenSearch **3.5.0** | NetApp Instaclustr managed, AI Search Plugin, 3 data nodes (m.80) |

Chapters 2 through 5 need the **AI Search Plugin** (ML Commons and k-NN). Chapter 4's MCP steps need OpenSearch **3.3 or later**. Chapter 4 Step 15 additionally needs **Node 18 or newer** on your own machine, not on the cluster.
