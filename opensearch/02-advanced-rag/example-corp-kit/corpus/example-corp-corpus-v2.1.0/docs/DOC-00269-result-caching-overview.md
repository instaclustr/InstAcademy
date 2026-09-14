---
source_id: "DOC-00269"
title: "Result Caching overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Result Caching > Result Caching overview"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2025-03-25"
related_error_codes: ["ERR-5501"]
---

# Result Caching overview

Result Caching lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

When result caching is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, result caching is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable result caching, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for result caching are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: result caching performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
