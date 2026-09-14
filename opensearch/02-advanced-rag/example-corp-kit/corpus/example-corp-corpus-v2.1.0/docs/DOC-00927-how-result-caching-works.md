---
source_id: "DOC-00927"
title: "How result caching works"
doc_type: "product-docs"
section_path: "SQL Workbench > Result Caching > How result caching works"
product_area: "sql-workbench"
product_version: "5.1"
acl: "public"
updated_at: "2025-06-29"
related_error_codes: ["ERR-5501"]
---

# How result caching works

Result Caching lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

To enable result caching, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

By default, result caching is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, result caching inherits group membership from your identity provider on each login.

Audit events for result caching are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: result caching performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
