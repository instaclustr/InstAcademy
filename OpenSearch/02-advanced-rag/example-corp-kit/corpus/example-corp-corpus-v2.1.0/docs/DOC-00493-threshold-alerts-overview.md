---
source_id: "DOC-00493"
title: "Threshold Alerts overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Threshold Alerts > Threshold Alerts overview"
product_area: "alerts"
product_version: "5.1"
acl: "public"
updated_at: "2025-04-13"
related_error_codes: ["ERR-4402"]
---

# Threshold Alerts overview

This page explains how threshold alerts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, threshold alerts inherits group membership from your identity provider on each login.

When threshold alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for threshold alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: threshold alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable threshold alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
