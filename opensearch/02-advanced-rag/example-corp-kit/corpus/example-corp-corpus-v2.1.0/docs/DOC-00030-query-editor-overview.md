---
source_id: "DOC-00030"
title: "Query Editor overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Editor > Query Editor overview"
product_area: "sql-workbench"
product_version: "5.1"
acl: "standard"
updated_at: "2026-06-11"
related_error_codes: ["ERR-5501"]
---

# Query Editor overview

Query Editor lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

By default, query editor is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable query editor, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for query editor are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: query editor performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When query editor is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
