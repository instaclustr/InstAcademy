---
source_id: "DOC-00092"
title: "How to configure workspace permissions"
doc_type: "product-docs"
section_path: "Administration > Workspace Permissions > How to configure workspace permissions"
product_area: "admin"
product_version: "4.9"
acl: "public"
updated_at: "2025-09-06"
related_error_codes: ["ERR-7719"]
---

# How to configure workspace permissions

This page explains how workspace permissions works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable workspace permissions, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

When workspace permissions is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: workspace permissions performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for workspace permissions are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, workspace permissions is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
