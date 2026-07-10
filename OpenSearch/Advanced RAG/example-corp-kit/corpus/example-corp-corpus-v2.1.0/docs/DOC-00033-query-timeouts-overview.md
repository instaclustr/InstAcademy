---
source_id: "DOC-00033"
title: "Query Timeouts overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Timeouts > Query Timeouts overview"
product_area: "sql-workbench"
product_version: "4.9"
acl: "public"
updated_at: "2025-04-11"
related_error_codes: ["ERR-5501"]
---

# Query Timeouts overview

Query Timeouts is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, query timeouts inherits group membership from your identity provider on each login.

When query timeouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: query timeouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, query timeouts is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for query timeouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
