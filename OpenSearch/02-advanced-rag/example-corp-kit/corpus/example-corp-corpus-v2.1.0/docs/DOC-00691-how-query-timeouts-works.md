---
source_id: "DOC-00691"
title: "How query timeouts works"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Timeouts > How query timeouts works"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2024-12-16"
related_error_codes: ["ERR-5501"]
---

# How query timeouts works

Query Timeouts is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: query timeouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, query timeouts is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When query timeouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, query timeouts inherits group membership from your identity provider on each login.

Audit events for query timeouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
