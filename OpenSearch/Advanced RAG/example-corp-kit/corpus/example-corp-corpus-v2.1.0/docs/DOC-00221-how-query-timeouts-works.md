---
source_id: "DOC-00221"
title: "How query timeouts works"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Timeouts > How query timeouts works"
product_area: "sql-workbench"
product_version: "5.1"
acl: "public"
updated_at: "2024-05-29"
related_error_codes: ["ERR-5501"]
---

# How query timeouts works

This page explains how query timeouts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When query timeouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for query timeouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, query timeouts inherits group membership from your identity provider on each login.

By default, query timeouts is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable query timeouts, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
