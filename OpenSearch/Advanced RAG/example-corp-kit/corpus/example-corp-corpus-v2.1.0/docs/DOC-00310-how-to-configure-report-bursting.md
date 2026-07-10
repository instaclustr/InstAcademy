---
source_id: "DOC-00310"
title: "How to configure report bursting"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Report Bursting > How to configure report bursting"
product_area: "alerts"
product_version: "5.1"
acl: "public"
updated_at: "2026-05-20"
related_error_codes: ["ERR-4415"]
---

# How to configure report bursting

Report Bursting is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable report bursting, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

When report bursting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, report bursting inherits group membership from your identity provider on each login.

By default, report bursting is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: report bursting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
