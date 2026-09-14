---
source_id: "DOC-00664"
title: "How PDF export works"
doc_type: "product-docs"
section_path: "Dashboards > Pdf Export > How PDF export works"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2025-12-10"
related_error_codes: ["ERR-1102", "ERR-1147"]
---

# How PDF export works

Pdf Export lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

Audit events for PDF export are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, PDF export is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable PDF export, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When PDF export is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: PDF export performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
