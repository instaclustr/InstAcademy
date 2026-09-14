---
source_id: "DOC-00452"
title: "How alert throttling works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Alert Throttling > How alert throttling works"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2025-02-21"
related_error_codes: ["ERR-4402"]
---

# How alert throttling works

Alert Throttling is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable alert throttling, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

By default, alert throttling is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When alert throttling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: alert throttling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, alert throttling inherits group membership from your identity provider on each login.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
