---
source_id: "DOC-00733"
title: "Report Bursting overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Report Bursting > Report Bursting overview"
product_area: "alerts"
product_version: "4.9"
acl: "public"
updated_at: "2026-05-28"
related_error_codes: ["ERR-4415"]
---

# Report Bursting overview

This page explains how report bursting works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, report bursting inherits group membership from your identity provider on each login.

When report bursting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable report bursting, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: report bursting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for report bursting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
