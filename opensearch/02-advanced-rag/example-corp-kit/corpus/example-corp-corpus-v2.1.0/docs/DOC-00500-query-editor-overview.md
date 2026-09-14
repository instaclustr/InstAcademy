---
source_id: "DOC-00500"
title: "Query Editor overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Editor > Query Editor overview"
product_area: "sql-workbench"
product_version: "4.9"
acl: "public"
updated_at: "2024-11-10"
related_error_codes: ["ERR-5501"]
---

# Query Editor overview

Query Editor lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

When query editor is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, query editor is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: query editor performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, query editor inherits group membership from your identity provider on each login.

Audit events for query editor are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
