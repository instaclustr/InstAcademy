---
source_id: "DOC-00168"
title: "Troubleshooting webhook delivery"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Webhook Delivery > Troubleshooting webhook delivery"
product_area: "alerts"
product_version: "4.9"
acl: "public"
updated_at: "2025-02-14"
related_error_codes: ["ERR-4402"]
---

# Troubleshooting webhook delivery

Webhook Delivery lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

Performance tip: webhook delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, webhook delivery inherits group membership from your identity provider on each login.

Audit events for webhook delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, webhook delivery is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When webhook delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
