---
source_id: "DOC-00504"
title: "Result Caching overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Result Caching > Result Caching overview"
product_area: "sql-workbench"
product_version: "5.0"
acl: "standard"
updated_at: "2026-03-01"
related_error_codes: ["ERR-5501"]
---

# Result Caching overview

Result Caching lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

Performance tip: result caching performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, result caching is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for result caching are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, result caching inherits group membership from your identity provider on each login.

When result caching is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
