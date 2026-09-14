---
source_id: "DOC-00922"
title: "How alert throttling works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Alert Throttling > How alert throttling works"
product_area: "alerts"
product_version: "4.9"
acl: "public"
updated_at: "2026-02-02"
related_error_codes: ["ERR-4402"]
---

# How alert throttling works

Alert Throttling lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

By default, alert throttling is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, alert throttling inherits group membership from your identity provider on each login.

Audit events for alert throttling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When alert throttling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable alert throttling, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
