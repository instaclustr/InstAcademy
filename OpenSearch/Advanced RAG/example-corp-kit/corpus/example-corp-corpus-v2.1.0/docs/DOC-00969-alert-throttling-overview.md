---
source_id: "DOC-00969"
title: "Alert Throttling overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Alert Throttling > Alert Throttling overview"
product_area: "alerts"
product_version: "4.9"
acl: "professional"
updated_at: "2025-03-09"
related_error_codes: ["ERR-4415"]
---

# Alert Throttling overview

This page explains how alert throttling works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable alert throttling, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: alert throttling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, alert throttling inherits group membership from your identity provider on each login.

By default, alert throttling is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When alert throttling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
