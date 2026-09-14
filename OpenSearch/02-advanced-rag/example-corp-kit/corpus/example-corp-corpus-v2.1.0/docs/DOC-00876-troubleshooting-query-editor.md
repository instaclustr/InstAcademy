---
source_id: "DOC-00876"
title: "Troubleshooting query editor"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Editor > Troubleshooting query editor"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2025-12-22"
related_error_codes: ["ERR-5501"]
---

# Troubleshooting query editor

Query Editor lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

To enable query editor, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

When query editor is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, query editor is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: query editor performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, query editor inherits group membership from your identity provider on each login.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
