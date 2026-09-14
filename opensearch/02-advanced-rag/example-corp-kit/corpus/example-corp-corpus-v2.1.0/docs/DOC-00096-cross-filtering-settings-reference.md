---
source_id: "DOC-00096"
title: "Cross-Filtering settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Cross-Filtering > Cross-Filtering settings reference"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2025-07-28"
related_error_codes: ["ERR-1102"]
---

# Cross-Filtering settings reference

Cross-Filtering is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for cross-filtering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable cross-filtering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When cross-filtering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: cross-filtering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, cross-filtering is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
