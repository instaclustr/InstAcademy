---
source_id: "DOC-00972"
title: "Saved Queries overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Saved Queries > Saved Queries overview"
product_area: "sql-workbench"
product_version: "4.8"
acl: "public"
updated_at: "2024-05-09"
related_error_codes: ["ERR-5501"]
---

# Saved Queries overview

Saved Queries is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: saved queries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, saved queries inherits group membership from your identity provider on each login.

To enable saved queries, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

When saved queries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for saved queries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
