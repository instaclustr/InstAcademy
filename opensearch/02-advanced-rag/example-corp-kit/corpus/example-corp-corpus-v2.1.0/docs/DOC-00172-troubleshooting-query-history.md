---
source_id: "DOC-00172"
title: "Troubleshooting query history"
doc_type: "product-docs"
section_path: "SQL Workbench > Query History > Troubleshooting query history"
product_area: "sql-workbench"
product_version: "4.9"
acl: "public"
updated_at: "2025-04-28"
related_error_codes: ["ERR-5501"]
---

# Troubleshooting query history

Query History is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for query history are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable query history, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

When query history is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, query history inherits group membership from your identity provider on each login.

Performance tip: query history performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
