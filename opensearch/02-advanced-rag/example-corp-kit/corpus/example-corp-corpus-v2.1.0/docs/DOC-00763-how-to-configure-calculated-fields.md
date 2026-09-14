---
source_id: "DOC-00763"
title: "How to configure calculated fields"
doc_type: "product-docs"
section_path: "Datasets > Calculated Fields > How to configure calculated fields"
product_area: "datasets"
product_version: "5.0"
acl: "public"
updated_at: "2025-06-30"
related_error_codes: ["ERR-3305", "ERR-3340"]
---

# How to configure calculated fields

Calculated Fields is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, calculated fields is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable calculated fields, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for calculated fields are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When calculated fields is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: calculated fields performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
