---
source_id: "DOC-00589"
title: "Email Delivery settings reference"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Email Delivery > Email Delivery settings reference"
product_area: "alerts"
product_version: "4.9"
acl: "public"
updated_at: "2024-02-14"
related_error_codes: ["ERR-4415", "ERR-4402"]
---

# Email Delivery settings reference

Email Delivery is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, email delivery inherits group membership from your identity provider on each login.

By default, email delivery is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When email delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for email delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: email delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
