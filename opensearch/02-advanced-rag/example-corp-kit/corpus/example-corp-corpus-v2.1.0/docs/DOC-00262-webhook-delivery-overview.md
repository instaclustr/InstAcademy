---
source_id: "DOC-00262"
title: "Webhook Delivery overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Webhook Delivery > Webhook Delivery overview"
product_area: "alerts"
product_version: "5.0"
acl: "public"
updated_at: "2025-07-26"
related_error_codes: ["ERR-4402"]
---

# Webhook Delivery overview

Webhook Delivery lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

Performance tip: webhook delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, webhook delivery is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for webhook delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When webhook delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, webhook delivery inherits group membership from your identity provider on each login.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
