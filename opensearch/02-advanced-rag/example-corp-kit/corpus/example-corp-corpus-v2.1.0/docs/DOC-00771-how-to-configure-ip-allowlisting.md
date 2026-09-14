---
source_id: "DOC-00771"
title: "How to configure IP allowlisting"
doc_type: "product-docs"
section_path: "Data Connectors > Ip Allowlisting > How to configure IP allowlisting"
product_area: "connectors"
product_version: "4.9"
acl: "public"
updated_at: "2025-05-04"
related_error_codes: ["ERR-2288", "ERR-2231"]
---

# How to configure IP allowlisting

This page explains how IP allowlisting works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, IP allowlisting is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When IP allowlisting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for IP allowlisting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: IP allowlisting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable IP allowlisting, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
