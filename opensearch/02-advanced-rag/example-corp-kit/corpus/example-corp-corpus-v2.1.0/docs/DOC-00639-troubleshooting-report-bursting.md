---
source_id: "DOC-00639"
title: "Troubleshooting report bursting"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Report Bursting > Troubleshooting report bursting"
product_area: "alerts"
product_version: "5.0"
acl: "professional"
updated_at: "2025-01-07"
related_error_codes: ["ERR-4415"]
---

# Troubleshooting report bursting

Report Bursting is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for report bursting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, report bursting inherits group membership from your identity provider on each login.

Performance tip: report bursting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When report bursting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable report bursting, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
