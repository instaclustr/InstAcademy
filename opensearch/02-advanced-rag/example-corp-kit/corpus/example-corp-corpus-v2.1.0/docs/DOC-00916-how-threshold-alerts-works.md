---
source_id: "DOC-00916"
title: "How threshold alerts works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Threshold Alerts > How threshold alerts works"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2026-06-05"
related_error_codes: ["ERR-4402"]
---

# How threshold alerts works

This page explains how threshold alerts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for threshold alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable threshold alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, threshold alerts inherits group membership from your identity provider on each login.

Performance tip: threshold alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When threshold alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
