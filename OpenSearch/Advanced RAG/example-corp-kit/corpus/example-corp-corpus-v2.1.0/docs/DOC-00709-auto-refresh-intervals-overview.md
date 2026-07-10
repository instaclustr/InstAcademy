---
source_id: "DOC-00709"
title: "Auto-Refresh Intervals overview"
doc_type: "product-docs"
section_path: "Dashboards > Auto-Refresh Intervals > Auto-Refresh Intervals overview"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2025-02-09"
related_error_codes: ["ERR-1102"]
---

# Auto-Refresh Intervals overview

Auto-Refresh Intervals is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When auto-refresh intervals is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for auto-refresh intervals are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: auto-refresh intervals performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable auto-refresh intervals, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

By default, auto-refresh intervals is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
