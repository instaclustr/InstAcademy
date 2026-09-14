---
source_id: "DOC-00072"
title: "How to configure email delivery"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Email Delivery > How to configure email delivery"
product_area: "alerts"
product_version: "4.9"
acl: "public"
updated_at: "2024-03-16"
related_error_codes: ["ERR-4415"]
---

# How to configure email delivery

Email Delivery is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When email delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable email delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: email delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, email delivery is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for email delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
