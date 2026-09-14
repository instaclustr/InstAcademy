---
source_id: "DOC-00450"
title: "How webhook delivery works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Webhook Delivery > How webhook delivery works"
product_area: "alerts"
product_version: "4.8"
acl: "standard"
updated_at: "2024-07-31"
related_error_codes: ["ERR-4402"]
---

# How webhook delivery works

Webhook Delivery lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

When webhook delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, webhook delivery inherits group membership from your identity provider on each login.

Audit events for webhook delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable webhook delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

By default, webhook delivery is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
