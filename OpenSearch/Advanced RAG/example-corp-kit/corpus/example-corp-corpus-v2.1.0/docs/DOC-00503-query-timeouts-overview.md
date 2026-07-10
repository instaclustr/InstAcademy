---
source_id: "DOC-00503"
title: "Query Timeouts overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Timeouts > Query Timeouts overview"
product_area: "sql-workbench"
product_version: "4.8"
acl: "public"
updated_at: "2025-09-19"
related_error_codes: ["ERR-5501"]
---

# Query Timeouts overview

Query Timeouts lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

When query timeouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for query timeouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable query timeouts, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: query timeouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, query timeouts is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
