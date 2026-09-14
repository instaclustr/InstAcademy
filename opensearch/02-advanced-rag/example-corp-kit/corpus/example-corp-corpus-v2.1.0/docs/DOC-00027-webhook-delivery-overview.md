---
source_id: "DOC-00027"
title: "Webhook Delivery overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Webhook Delivery > Webhook Delivery overview"
product_area: "alerts"
product_version: "5.1"
acl: "public"
updated_at: "2024-07-20"
related_error_codes: ["ERR-4415"]
---

# Webhook Delivery overview

Webhook Delivery is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable webhook delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: webhook delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for webhook delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, webhook delivery is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When webhook delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
