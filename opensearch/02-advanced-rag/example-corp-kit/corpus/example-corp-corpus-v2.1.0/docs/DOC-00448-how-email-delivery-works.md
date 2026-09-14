---
source_id: "DOC-00448"
title: "How email delivery works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Email Delivery > How email delivery works"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2025-06-06"
related_error_codes: ["ERR-4415", "ERR-4402"]
---

# How email delivery works

Email Delivery is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, email delivery inherits group membership from your identity provider on each login.

By default, email delivery is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for email delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: email delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When email delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
