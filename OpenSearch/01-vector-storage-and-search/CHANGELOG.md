← [Course index](README.md) · [How to run labs](HANDS-ON-GUIDE.md) · [Cluster setup](CLUSTER-SETUP.md)

# Changelog

All notable changes to this course are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the course uses [semantic versioning](https://semver.org/) adapted for learning material:

- **Major** (2.0.0): a restructure that changes the chapter or lesson lineup, so anyone mid-course would need to restart.
- **Minor** (1.1.0): steps added, removed, or renumbered inside a chapter, or a new OpenSearch version validated.
- **Patch** (1.0.1): corrections, clearer wording, updated screenshots, no change to what you run.

## [1.0] — 2026-07-15

Initial release. The course is complete and published: five chapters of hands-on workshops, validated end to end against a live OpenSearch 3.5.0 cluster.

## 📋 Compatibility

| Course version | Validated on | Cluster |
|---|---|---|
| 1.0 | OpenSearch **3.5.0** | NetApp Instaclustr managed, AI Search Plugin, 3 data nodes (m.80) |

Chapters 2 through 5 need the **AI Search Plugin** (ML Commons and k-NN). Chapter 4's MCP steps need OpenSearch **3.3 or later**. Chapter 4's Claude Desktop step additionally needs **Node 18 or newer** on your own machine, not on the cluster.
