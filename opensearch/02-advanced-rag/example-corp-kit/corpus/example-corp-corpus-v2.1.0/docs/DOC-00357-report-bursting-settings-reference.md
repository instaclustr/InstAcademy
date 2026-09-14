---
source_id: "DOC-00357"
title: "Report Bursting settings reference"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Report Bursting > Report Bursting settings reference"
product_area: "alerts"
product_version: "4.9"
acl: "standard"
updated_at: "2024-05-20"
related_error_codes: ["ERR-4415"]
---

# Report Bursting settings reference

This page explains how report bursting works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, report bursting is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: report bursting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for report bursting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, report bursting inherits group membership from your identity provider on each login.

When report bursting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
