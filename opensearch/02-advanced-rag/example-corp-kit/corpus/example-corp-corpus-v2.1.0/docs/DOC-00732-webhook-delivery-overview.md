---
source_id: "DOC-00732"
title: "Webhook Delivery overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Webhook Delivery > Webhook Delivery overview"
product_area: "alerts"
product_version: "4.9"
acl: "public"
updated_at: "2024-10-13"
related_error_codes: ["ERR-4415"]
---

# Webhook Delivery overview

This page explains how webhook delivery works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for webhook delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When webhook delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: webhook delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable webhook delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, webhook delivery inherits group membership from your identity provider on each login.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
