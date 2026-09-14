---
source_id: "DOC-00169"
title: "Troubleshooting report bursting"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Report Bursting > Troubleshooting report bursting"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2024-09-27"
related_error_codes: ["ERR-4415", "ERR-4402"]
---

# Troubleshooting report bursting

Report Bursting lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

When report bursting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, report bursting inherits group membership from your identity provider on each login.

By default, report bursting is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable report bursting, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: report bursting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
