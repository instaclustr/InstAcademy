---
source_id: "DOC-00097"
title: "Drill-Down settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Drill-Down > Drill-Down settings reference"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2026-01-25"
related_error_codes: ["ERR-1147"]
---

# Drill-Down settings reference

Drill-Down is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When drill-down is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: drill-down performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for drill-down are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, drill-down inherits group membership from your identity provider on each login.

To enable drill-down, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
