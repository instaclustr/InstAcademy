---
source_id: "DOC-00921"
title: "How report bursting works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Report Bursting > How report bursting works"
product_area: "alerts"
product_version: "4.8"
acl: "enterprise"
updated_at: "2025-07-03"
related_error_codes: ["ERR-4415", "ERR-4402"]
---

# How report bursting works

Report Bursting is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for report bursting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, report bursting inherits group membership from your identity provider on each login.

By default, report bursting is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When report bursting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable report bursting, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
