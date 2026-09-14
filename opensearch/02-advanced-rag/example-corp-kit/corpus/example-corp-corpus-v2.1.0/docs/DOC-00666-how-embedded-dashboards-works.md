---
source_id: "DOC-00666"
title: "How embedded dashboards works"
doc_type: "product-docs"
section_path: "Dashboards > Embedded Dashboards > How embedded dashboards works"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2024-11-05"
related_error_codes: ["ERR-1102"]
---

# How embedded dashboards works

Embedded Dashboards is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for embedded dashboards are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable embedded dashboards, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When embedded dashboards is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: embedded dashboards performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, embedded dashboards is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
