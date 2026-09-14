---
source_id: "DOC-00032"
title: "Saved Queries overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Saved Queries > Saved Queries overview"
product_area: "sql-workbench"
product_version: "5.0"
acl: "enterprise"
updated_at: "2024-02-11"
related_error_codes: ["ERR-5501"]
---

# Saved Queries overview

Saved Queries is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for saved queries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable saved queries, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

When saved queries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: saved queries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, saved queries is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
