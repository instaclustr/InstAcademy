---
source_id: "DOC-00536"
title: "How to configure IP allowlisting"
doc_type: "product-docs"
section_path: "Data Connectors > Ip Allowlisting > How to configure IP allowlisting"
product_area: "connectors"
product_version: "4.9"
acl: "public"
updated_at: "2025-10-09"
related_error_codes: ["ERR-2288"]
---

# How to configure IP allowlisting

This page explains how IP allowlisting works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, IP allowlisting is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, IP allowlisting inherits group membership from your identity provider on each login.

Audit events for IP allowlisting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable IP allowlisting, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

When IP allowlisting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
