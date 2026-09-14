---
source_id: "DOC-00636"
title: "Troubleshooting email delivery"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Email Delivery > Troubleshooting email delivery"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2026-06-26"
related_error_codes: ["ERR-4415"]
---

# Troubleshooting email delivery

This page explains how email delivery works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable email delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for email delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When email delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, email delivery inherits group membership from your identity provider on each login.

Performance tip: email delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
