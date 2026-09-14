---
source_id: "DOC-00336"
title: "Mobile Layouts settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Mobile Layouts > Mobile Layouts settings reference"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2024-09-23"
related_error_codes: ["ERR-1102", "ERR-1147"]
---

# Mobile Layouts settings reference

Mobile Layouts is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable mobile layouts, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: mobile layouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, mobile layouts is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When mobile layouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for mobile layouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
