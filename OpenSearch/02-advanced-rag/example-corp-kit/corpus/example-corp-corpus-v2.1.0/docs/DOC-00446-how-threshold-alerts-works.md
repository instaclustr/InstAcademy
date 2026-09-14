---
source_id: "DOC-00446"
title: "How threshold alerts works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Threshold Alerts > How threshold alerts works"
product_area: "alerts"
product_version: "5.0"
acl: "professional"
updated_at: "2025-04-17"
related_error_codes: ["ERR-4415"]
---

# How threshold alerts works

Threshold Alerts is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: threshold alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, threshold alerts inherits group membership from your identity provider on each login.

When threshold alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, threshold alerts is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for threshold alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
