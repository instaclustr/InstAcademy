---
source_id: "DOC-00681"
title: "How threshold alerts works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Threshold Alerts > How threshold alerts works"
product_area: "alerts"
product_version: "5.1"
acl: "public"
updated_at: "2026-01-18"
related_error_codes: ["ERR-4402"]
---

# How threshold alerts works

Threshold Alerts is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When threshold alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, threshold alerts is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, threshold alerts inherits group membership from your identity provider on each login.

Audit events for threshold alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: threshold alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
