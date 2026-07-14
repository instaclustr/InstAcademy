# InstAcademy · OpenSearch

**Optimizing OpenSearch Vector Storage and Search for Faster AI Applications**

Short label: **Vector Storage & Search for AI** — hands-on labs for this InstAcademy course.

**Course version 1.0.0** · validated end to end on **OpenSearch 3.5.0** · see the [changelog](CHANGELOG.md)

## Start here

1. **[How to run the labs](HANDS-ON-GUIDE.md)** — Dev Tools walkthrough, Bruno fast mode, credentials, sample data (read this first).
2. **[Cluster setup](CLUSTER-SETUP.md)** — sign up, create a trial cluster with the AI Search Plugin, open the firewall, and collect your connection details.
3. **[Chapter 1](src/Chapter%201/README.md)** — verify connectivity and build your first vector index.

| | |
|---|---|
| **Up to OpenSearch courses** | [OpenSearch/](../) |
| **Up to InstAcademy home** | [InstAcademy/](../../) |

## Chapters

| Chapter | Topic | Entry |
|---------|--------|--------|
| 1 | Vector fundamentals | [Chapter 1](src/Chapter%201/README.md) |
| 2 | Neural search pipelines | [Chapter 2](src/Chapter%202/README.md) |
| 3 | Hybrid / sparse search | [Chapter 3](src/Chapter%203/README.md) |
| 4 | RAG optimization | [Chapter 4](src/Chapter%204/README.md) |
| 5 | Production cluster ops | [Chapter 5](src/Chapter%205/README.md) |

## What's in this folder

| Path | For learners |
|------|----------------|
| [`HANDS-ON-GUIDE.md`](HANDS-ON-GUIDE.md) | How to read a chapter workshop and run the course |
| [`src/Chapter …/`](src/Chapter%201/) | One step-by-step Dev Tools workshop README per chapter |
| [`bruno/`](bruno/) | Fast-mode REST collection |
| [`rest/bulk/`](rest/bulk/) | NDJSON bulk payloads (the shared Gutendex book dataset) |
| [`CHANGELOG.md`](CHANGELOG.md) | What changed between course versions, and which OpenSearch version each was validated on |
| [`CLUSTER-SETUP.md`](CLUSTER-SETUP.md) | Sign up, create the cluster, open the firewall, collect connection details |

## For contributors

| Path | What it's for |
|------|----------------|
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to report a broken step and the house rules for changes |
| [`SECURITY.md`](SECURITY.md) | Credential handling, and which lab shortcuts are not production practice |
| [`scripts/validate.sh`](scripts/validate.sh) | Checks the collection, bulk payloads, links, and credentials before you commit |

## Support

[Instaclustr open-source project status](https://www.instaclustr.com/support/documentation/announcements/instaclustr-open-source-project-status/)
