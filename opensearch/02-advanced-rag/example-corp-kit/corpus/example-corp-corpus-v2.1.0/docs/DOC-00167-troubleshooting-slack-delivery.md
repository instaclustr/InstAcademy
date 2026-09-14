---
source_id: "DOC-00167"
title: "Troubleshooting Slack delivery"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Slack Delivery > Troubleshooting Slack delivery"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2024-01-21"
related_error_codes: ["ERR-4402"]
---

# Troubleshooting Slack delivery

Slack Delivery lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

When Slack delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: Slack delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for Slack delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable Slack delivery, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

By default, Slack delivery is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
