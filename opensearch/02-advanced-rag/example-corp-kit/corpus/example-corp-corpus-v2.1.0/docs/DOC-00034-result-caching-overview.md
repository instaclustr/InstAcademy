---
source_id: "DOC-00034"
title: "Result Caching overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Result Caching > Result Caching overview"
product_area: "sql-workbench"
product_version: "4.8"
acl: "public"
updated_at: "2025-02-09"
related_error_codes: ["ERR-5501"]
---

# Result Caching overview

Result Caching lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

By default, result caching is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When result caching is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for result caching are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, result caching inherits group membership from your identity provider on each login.

Performance tip: result caching performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
