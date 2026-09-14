---
source_id: "DOC-00642"
title: "Troubleshooting query history"
doc_type: "product-docs"
section_path: "SQL Workbench > Query History > Troubleshooting query history"
product_area: "sql-workbench"
product_version: "4.9"
acl: "public"
updated_at: "2025-11-16"
related_error_codes: ["ERR-5501"]
---

# Troubleshooting query history

Query History lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

By default, query history is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: query history performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, query history inherits group membership from your identity provider on each login.

When query history is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable query history, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
