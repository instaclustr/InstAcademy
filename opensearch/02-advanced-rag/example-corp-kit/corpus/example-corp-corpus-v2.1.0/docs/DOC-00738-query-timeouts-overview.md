---
source_id: "DOC-00738"
title: "Query Timeouts overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Timeouts > Query Timeouts overview"
product_area: "sql-workbench"
product_version: "5.1"
acl: "public"
updated_at: "2026-02-14"
related_error_codes: ["ERR-5501"]
---

# Query Timeouts overview

Query Timeouts is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: query timeouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When query timeouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, query timeouts is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable query timeouts, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for query timeouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
