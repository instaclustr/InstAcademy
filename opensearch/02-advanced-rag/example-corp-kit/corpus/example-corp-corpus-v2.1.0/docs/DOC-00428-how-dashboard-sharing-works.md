---
source_id: "DOC-00428"
title: "How dashboard sharing works"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Sharing > How dashboard sharing works"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2024-09-26"
related_error_codes: ["ERR-1102"]
---

# How dashboard sharing works

Dashboard Sharing lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

To enable dashboard sharing, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

By default, dashboard sharing is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: dashboard sharing performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for dashboard sharing are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When dashboard sharing is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
