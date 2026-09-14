---
source_id: "DOC-00869"
title: "Troubleshooting threshold alerts"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Threshold Alerts > Troubleshooting threshold alerts"
product_area: "alerts"
product_version: "5.1"
acl: "public"
updated_at: "2025-06-09"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# Troubleshooting threshold alerts

Threshold Alerts is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, threshold alerts is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, threshold alerts inherits group membership from your identity provider on each login.

To enable threshold alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: threshold alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When threshold alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
