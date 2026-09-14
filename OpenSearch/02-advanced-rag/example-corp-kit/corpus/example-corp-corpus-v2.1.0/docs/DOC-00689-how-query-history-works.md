---
source_id: "DOC-00689"
title: "How query history works"
doc_type: "product-docs"
section_path: "SQL Workbench > Query History > How query history works"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2025-04-14"
related_error_codes: ["ERR-5501"]
---

# How query history works

Query History is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, query history is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When query history is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for query history are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: query history performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, query history inherits group membership from your identity provider on each login.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
