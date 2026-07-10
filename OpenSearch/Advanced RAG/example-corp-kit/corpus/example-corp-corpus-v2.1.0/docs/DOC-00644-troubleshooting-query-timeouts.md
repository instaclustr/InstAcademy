---
source_id: "DOC-00644"
title: "Troubleshooting query timeouts"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Timeouts > Troubleshooting query timeouts"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2024-02-19"
related_error_codes: ["ERR-5501"]
---

# Troubleshooting query timeouts

This page explains how query timeouts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for query timeouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable query timeouts, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: query timeouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, query timeouts inherits group membership from your identity provider on each login.

By default, query timeouts is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
