---
source_id: "DOC-00023"
title: "Threshold Alerts overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Threshold Alerts > Threshold Alerts overview"
product_area: "alerts"
product_version: "5.0"
acl: "public"
updated_at: "2025-11-27"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# Threshold Alerts overview

Threshold Alerts is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, threshold alerts inherits group membership from your identity provider on each login.

When threshold alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: threshold alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, threshold alerts is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for threshold alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
