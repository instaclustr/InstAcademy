# InstAcademy · OpenSearch

**Optimizing OpenSearch Vector Storage and Search for Faster AI Applications**

Hands-on labs for this InstAcademy course. Work through lessons in **Dev Tools** (recommended) or use the **Bruno** fast-mode collection.

| Navigate | Link |
|----------|------|
| **Up to OpenSearch courses** | [OpenSearch/](../) |
| **Up to InstAcademy home** | [InstAcademy/](../../) |
| **How to read a lesson** | [docs/HANDS-ON-GUIDE.md](docs/HANDS-ON-GUIDE.md) |
| **Cluster setup (Instaclustr trial)** | [CREATE_CLUSTER.md](CREATE_CLUSTER.md) |
| **Formatted web guide** | [instaclustr.github.io/InstAcademy](https://instaclustr.github.io/InstAcademy/) |
| **Voice script** | [course script.docx](OpenSearch%20Learning%20Path%201.docx) |

The voice script is [`Optimizing OpenSearch Vector Storage and Search for Faster AI Applications (script).docx`](OpenSearch%20Learning%20Path%201.docx). Each lesson README under `src/Chapter …` follows that narrative.

## How to use this course

### Learn mode (start here)

Follow step-by-step **Dev Tools** instructions in each lesson README:

1. Install Python 3 (optional — only for sample-data download and reference scripts).
2. Provision a **3-node Instaclustr trial** with the **AI Search Plugin** ([CREATE_CLUSTER.md](CREATE_CLUSTER.md)).
3. Read [How to read a lesson](docs/HANDS-ON-GUIDE.md#how-to-read-a-lesson) (bold labels: **Step**, **Why**, **Request**, **Expected**, **Save**).
4. Start at [Chapter 1 Lesson 1](src/Chapter%201/1-1/README.md) — connectivity and sample data.
5. Continue chapter by chapter in **Lab steps** order.

### Fast mode (Bruno)

Use the [`bruno/`](bruno/) collection to run the same REST calls with less typing — recovery, catch-up, or smoke tests. See [bruno/README.md](bruno/README.md) (set `baseUrl`, credentials, **SSL verify off**).

## Course layout

| Path | Purpose |
|------|---------|
| [`src/Chapter 1/`](src/Chapter%201) | Connectivity, keyword index, vector reindex |
| [`src/Chapter 2/`](src/Chapter%202) | ML Commons, neural ingest pipeline, search |
| [`src/Chapter 3/`](src/Chapter%203) | Neural sparse + hybrid search |
| [`src/Chapter 4/`](src/Chapter%204) | Bookstore RAG, index tuning, query optimization |
| [`src/Chapter 5/`](src/Chapter%205) | Production cluster operations |
| [`rest/bulk/`](rest/bulk/) | NDJSON bulk payloads for Dev Tools / Bruno |
| [`bruno/`](bruno/) | Fast-mode REST collection |
| [`tools/`](tools/) | Generators for bulk NDJSON and Bruno requests |
| [`src/.env.example`](src/.env.example) | Optional env vars for Python reference scripts |

## Optional Python scripts

Fully commented `.py` files mirror the REST steps. Shared connection helpers live in [`src/utils/`](src/utils/). Copy `src/.env.example` → `src/.env` if you use them.

Regenerate bulk/Bruno assets after changing sample data:

```bash
python tools/generate-bulk-ndjson.py
python tools/generate-bruno-requests.py
```

Build the docs site locally (from this course folder):

```bash
pip install -r requirements-docs.txt
python tools/sync-mkdocs-content.py
mkdocs serve
```

Open [http://127.0.0.1:8000/InstAcademy/](http://127.0.0.1:8000/InstAcademy/) when the dev server starts.

## Support

[Instaclustr open-source project status](https://www.instaclustr.com/support/documentation/announcements/instaclustr-open-source-project-status/)
