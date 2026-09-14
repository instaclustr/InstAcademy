---
source_id: "DOC-00964"
title: "Anomaly Alerts overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Anomaly Alerts > Anomaly Alerts overview"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2026-04-28"
related_error_codes: ["ERR-4402"]
---

# Anomaly Alerts overview

This page explains how anomaly alerts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, anomaly alerts inherits group membership from your identity provider on each login.

By default, anomaly alerts is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When anomaly alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable anomaly alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for anomaly alerts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
