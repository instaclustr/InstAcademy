---
source_id: "DOC-00872"
title: "Troubleshooting Slack delivery"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Slack Delivery > Troubleshooting Slack delivery"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2024-03-22"
related_error_codes: ["ERR-4402"]
---

# Troubleshooting Slack delivery

Slack Delivery is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When Slack delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, Slack delivery inherits group membership from your identity provider on each login.

By default, Slack delivery is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable Slack delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: Slack delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
