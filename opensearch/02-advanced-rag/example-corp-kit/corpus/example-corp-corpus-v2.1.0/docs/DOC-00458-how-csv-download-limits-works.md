---
source_id: "DOC-00458"
title: "How CSV download limits works"
doc_type: "product-docs"
section_path: "SQL Workbench > Csv Download Limits > How CSV download limits works"
product_area: "sql-workbench"
product_version: "4.8"
acl: "public"
updated_at: "2025-04-20"
related_error_codes: ["ERR-5501"]
---

# How CSV download limits works

This page explains how CSV download limits works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: CSV download limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable CSV download limits, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

By default, CSV download limits is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When CSV download limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for CSV download limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
