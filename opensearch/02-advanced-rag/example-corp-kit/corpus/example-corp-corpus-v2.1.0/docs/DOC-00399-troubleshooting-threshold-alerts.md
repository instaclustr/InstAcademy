---
source_id: "DOC-00399"
title: "Troubleshooting threshold alerts"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Threshold Alerts > Troubleshooting threshold alerts"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2026-06-20"
related_error_codes: ["ERR-4402"]
---

# Troubleshooting threshold alerts

Threshold Alerts lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

By default, threshold alerts is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When threshold alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: threshold alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, threshold alerts inherits group membership from your identity provider on each login.

Audit events for threshold alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
