---
source_id: "DOC-00219"
title: "How query history works"
doc_type: "product-docs"
section_path: "SQL Workbench > Query History > How query history works"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2024-02-07"
related_error_codes: ["ERR-5501"]
---

# How query history works

This page explains how query history works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, query history is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for query history are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, query history inherits group membership from your identity provider on each login.

When query history is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable query history, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
