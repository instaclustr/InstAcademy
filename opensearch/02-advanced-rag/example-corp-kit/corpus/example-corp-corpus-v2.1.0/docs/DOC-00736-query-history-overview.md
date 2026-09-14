---
source_id: "DOC-00736"
title: "Query History overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Query History > Query History overview"
product_area: "sql-workbench"
product_version: "4.8"
acl: "public"
updated_at: "2026-04-10"
related_error_codes: ["ERR-5501"]
---

# Query History overview

Query History is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, query history is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable query history, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: query history performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for query history are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When query history is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
