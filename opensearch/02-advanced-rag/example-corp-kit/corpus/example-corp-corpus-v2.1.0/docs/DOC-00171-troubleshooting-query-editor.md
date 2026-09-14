---
source_id: "DOC-00171"
title: "Troubleshooting query editor"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Editor > Troubleshooting query editor"
product_area: "sql-workbench"
product_version: "4.8"
acl: "public"
updated_at: "2024-08-30"
related_error_codes: ["ERR-5501"]
---

# Troubleshooting query editor

Query Editor lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

To enable query editor, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: query editor performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for query editor are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, query editor is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, query editor inherits group membership from your identity provider on each login.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
