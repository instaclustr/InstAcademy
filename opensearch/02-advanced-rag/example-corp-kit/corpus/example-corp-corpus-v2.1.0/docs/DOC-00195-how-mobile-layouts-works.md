---
source_id: "DOC-00195"
title: "How mobile layouts works"
doc_type: "product-docs"
section_path: "Dashboards > Mobile Layouts > How mobile layouts works"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2025-10-17"
related_error_codes: ["ERR-1210", "ERR-1102"]
---

# How mobile layouts works

Mobile Layouts lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Audit events for mobile layouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: mobile layouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When mobile layouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, mobile layouts is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable mobile layouts, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
