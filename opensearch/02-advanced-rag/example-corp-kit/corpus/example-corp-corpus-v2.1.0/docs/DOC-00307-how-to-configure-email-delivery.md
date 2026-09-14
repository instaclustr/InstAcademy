---
source_id: "DOC-00307"
title: "How to configure email delivery"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Email Delivery > How to configure email delivery"
product_area: "alerts"
product_version: "5.0"
acl: "public"
updated_at: "2025-12-19"
related_error_codes: ["ERR-4415"]
---

# How to configure email delivery

Email Delivery lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

Audit events for email delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When email delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: email delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, email delivery inherits group membership from your identity provider on each login.

By default, email delivery is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
