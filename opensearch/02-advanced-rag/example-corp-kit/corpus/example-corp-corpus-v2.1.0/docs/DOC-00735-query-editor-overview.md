---
source_id: "DOC-00735"
title: "Query Editor overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Editor > Query Editor overview"
product_area: "sql-workbench"
product_version: "4.8"
acl: "public"
updated_at: "2025-05-24"
related_error_codes: ["ERR-5501"]
---

# Query Editor overview

Query Editor is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, query editor inherits group membership from your identity provider on each login.

Performance tip: query editor performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for query editor are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, query editor is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When query editor is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
