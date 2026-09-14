---
source_id: "DOC-00659"
title: "How dashboard rendering works"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Rendering > How dashboard rendering works"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2025-03-28"
related_error_codes: ["ERR-1147", "ERR-1102"]
---

# How dashboard rendering works

This page explains how dashboard rendering works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When dashboard rendering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: dashboard rendering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable dashboard rendering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

By default, dashboard rendering is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for dashboard rendering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
