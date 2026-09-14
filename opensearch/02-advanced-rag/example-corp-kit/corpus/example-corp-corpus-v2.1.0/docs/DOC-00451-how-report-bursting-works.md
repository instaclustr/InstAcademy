---
source_id: "DOC-00451"
title: "How report bursting works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Report Bursting > How report bursting works"
product_area: "alerts"
product_version: "5.1"
acl: "public"
updated_at: "2026-03-21"
related_error_codes: ["ERR-4402", "ERR-4415"]
---

# How report bursting works

Report Bursting is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When report bursting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, report bursting inherits group membership from your identity provider on each login.

Performance tip: report bursting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable report bursting, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for report bursting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
