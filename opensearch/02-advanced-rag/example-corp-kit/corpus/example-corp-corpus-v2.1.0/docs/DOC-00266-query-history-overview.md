---
source_id: "DOC-00266"
title: "Query History overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Query History > Query History overview"
product_area: "sql-workbench"
product_version: "4.8"
acl: "public"
updated_at: "2025-08-19"
related_error_codes: ["ERR-5501"]
---

# Query History overview

Query History is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When query history is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable query history, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for query history are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, query history inherits group membership from your identity provider on each login.

By default, query history is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
