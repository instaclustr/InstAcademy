---
source_id: "DOC-00877"
title: "Troubleshooting query history"
doc_type: "product-docs"
section_path: "SQL Workbench > Query History > Troubleshooting query history"
product_area: "sql-workbench"
product_version: "5.1"
acl: "enterprise"
updated_at: "2025-10-11"
related_error_codes: ["ERR-5501"]
---

# Troubleshooting query history

Query History lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

Audit events for query history are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When query history is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, query history inherits group membership from your identity provider on each login.

Performance tip: query history performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, query history is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
