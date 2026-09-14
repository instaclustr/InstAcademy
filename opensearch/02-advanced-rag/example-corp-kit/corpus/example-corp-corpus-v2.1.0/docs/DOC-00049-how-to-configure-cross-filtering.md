---
source_id: "DOC-00049"
title: "How to configure cross-filtering"
doc_type: "product-docs"
section_path: "Dashboards > Cross-Filtering > How to configure cross-filtering"
product_area: "dashboards"
product_version: "4.8"
acl: "enterprise"
updated_at: "2025-11-02"
related_error_codes: ["ERR-1102"]
---

# How to configure cross-filtering

Cross-Filtering is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, cross-filtering is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable cross-filtering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: cross-filtering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for cross-filtering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When cross-filtering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
