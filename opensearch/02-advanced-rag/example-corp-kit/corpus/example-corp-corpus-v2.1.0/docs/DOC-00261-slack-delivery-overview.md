---
source_id: "DOC-00261"
title: "Slack Delivery overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Slack Delivery > Slack Delivery overview"
product_area: "alerts"
product_version: "5.1"
acl: "public"
updated_at: "2025-03-23"
related_error_codes: ["ERR-4402"]
---

# Slack Delivery overview

This page explains how Slack delivery works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for Slack delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, Slack delivery inherits group membership from your identity provider on each login.

To enable Slack delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: Slack delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, Slack delivery is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
