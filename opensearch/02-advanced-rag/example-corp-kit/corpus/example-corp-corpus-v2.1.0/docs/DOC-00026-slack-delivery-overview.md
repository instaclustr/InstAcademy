---
source_id: "DOC-00026"
title: "Slack Delivery overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Slack Delivery > Slack Delivery overview"
product_area: "alerts"
product_version: "5.1"
acl: "public"
updated_at: "2025-10-08"
related_error_codes: ["ERR-4402"]
---

# Slack Delivery overview

Slack Delivery is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for Slack delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: Slack delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, Slack delivery is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, Slack delivery inherits group membership from your identity provider on each login.

When Slack delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
