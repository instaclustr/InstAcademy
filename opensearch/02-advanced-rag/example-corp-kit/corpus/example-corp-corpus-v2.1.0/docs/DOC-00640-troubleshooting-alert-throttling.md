---
source_id: "DOC-00640"
title: "Troubleshooting alert throttling"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Alert Throttling > Troubleshooting alert throttling"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2025-02-12"
related_error_codes: ["ERR-4415"]
---

# Troubleshooting alert throttling

This page explains how alert throttling works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: alert throttling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for alert throttling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, alert throttling inherits group membership from your identity provider on each login.

By default, alert throttling is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When alert throttling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.
