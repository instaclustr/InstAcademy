---
source_id: "DOC-00218"
title: "How query editor works"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Editor > How query editor works"
product_area: "sql-workbench"
product_version: "4.9"
acl: "professional"
updated_at: "2025-06-07"
related_error_codes: ["ERR-5501"]
---

# How query editor works

Query Editor lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

When query editor is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for query editor are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, query editor inherits group membership from your identity provider on each login.

To enable query editor, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

By default, query editor is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
