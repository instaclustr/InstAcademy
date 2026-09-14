---
source_id: "DOC-00947"
title: "Mobile Layouts overview"
doc_type: "product-docs"
section_path: "Dashboards > Mobile Layouts > Mobile Layouts overview"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2024-09-11"
related_error_codes: ["ERR-1147", "ERR-1102"]
---

# Mobile Layouts overview

Mobile Layouts lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

To enable mobile layouts, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

By default, mobile layouts is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for mobile layouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When mobile layouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: mobile layouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
