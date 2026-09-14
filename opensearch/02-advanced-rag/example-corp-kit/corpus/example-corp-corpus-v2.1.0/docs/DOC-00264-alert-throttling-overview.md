---
source_id: "DOC-00264"
title: "Alert Throttling overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Alert Throttling > Alert Throttling overview"
product_area: "alerts"
product_version: "4.8"
acl: "professional"
updated_at: "2025-02-20"
related_error_codes: ["ERR-4415"]
---

# Alert Throttling overview

Alert Throttling is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: alert throttling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for alert throttling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When alert throttling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, alert throttling is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, alert throttling inherits group membership from your identity provider on each login.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
