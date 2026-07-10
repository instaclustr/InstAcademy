---
source_id: "DOC-00968"
title: "Report Bursting overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Report Bursting > Report Bursting overview"
product_area: "alerts"
product_version: "5.0"
acl: "public"
updated_at: "2024-07-05"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# Report Bursting overview

This page explains how report bursting works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: report bursting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, report bursting inherits group membership from your identity provider on each login.

To enable report bursting, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

When report bursting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for report bursting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
