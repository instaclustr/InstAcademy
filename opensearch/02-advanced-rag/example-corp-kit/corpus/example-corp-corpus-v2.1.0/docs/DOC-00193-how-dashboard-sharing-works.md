---
source_id: "DOC-00193"
title: "How dashboard sharing works"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Sharing > How dashboard sharing works"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2025-03-02"
related_error_codes: ["ERR-1210", "ERR-1102"]
---

# How dashboard sharing works

Dashboard Sharing is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, dashboard sharing is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: dashboard sharing performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When dashboard sharing is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for dashboard sharing are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable dashboard sharing, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
