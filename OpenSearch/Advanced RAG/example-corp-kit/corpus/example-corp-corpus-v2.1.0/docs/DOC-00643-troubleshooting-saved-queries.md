---
source_id: "DOC-00643"
title: "Troubleshooting saved queries"
doc_type: "product-docs"
section_path: "SQL Workbench > Saved Queries > Troubleshooting saved queries"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2024-02-24"
related_error_codes: ["ERR-5501"]
---

# Troubleshooting saved queries

Saved Queries lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

By default, saved queries is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for saved queries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, saved queries inherits group membership from your identity provider on each login.

When saved queries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: saved queries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
