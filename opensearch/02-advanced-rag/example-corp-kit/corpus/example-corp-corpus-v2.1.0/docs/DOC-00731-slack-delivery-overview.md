---
source_id: "DOC-00731"
title: "Slack Delivery overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Slack Delivery > Slack Delivery overview"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2025-04-10"
related_error_codes: ["ERR-4415"]
---

# Slack Delivery overview

This page explains how Slack delivery works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: Slack delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, Slack delivery inherits group membership from your identity provider on each login.

To enable Slack delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

By default, Slack delivery is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When Slack delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
