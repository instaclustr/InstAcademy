---
source_id: "DOC-00638"
title: "Troubleshooting webhook delivery"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Webhook Delivery > Troubleshooting webhook delivery"
product_area: "alerts"
product_version: "5.0"
acl: "enterprise"
updated_at: "2025-03-22"
related_error_codes: ["ERR-4402"]
---

# Troubleshooting webhook delivery

Webhook Delivery is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: webhook delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable webhook delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for webhook delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, webhook delivery is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, webhook delivery inherits group membership from your identity provider on each login.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
