---
source_id: "DOC-00290"
title: "How to configure embedded dashboards"
doc_type: "product-docs"
section_path: "Dashboards > Embedded Dashboards > How to configure embedded dashboards"
product_area: "dashboards"
product_version: "5.1"
acl: "enterprise"
updated_at: "2025-12-30"
related_error_codes: ["ERR-1102"]
---

# How to configure embedded dashboards

This page explains how embedded dashboards works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, embedded dashboards is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for embedded dashboards are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: embedded dashboards performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable embedded dashboards, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When embedded dashboards is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
