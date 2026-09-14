---
source_id: "DOC-00404"
title: "Troubleshooting report bursting"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Report Bursting > Troubleshooting report bursting"
product_area: "alerts"
product_version: "4.9"
acl: "public"
updated_at: "2025-05-06"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# Troubleshooting report bursting

Report Bursting is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable report bursting, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for report bursting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, report bursting is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: report bursting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, report bursting inherits group membership from your identity provider on each login.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
