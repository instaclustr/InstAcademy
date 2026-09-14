---
source_id: "DOC-00149"
title: "Troubleshooting embedded dashboards"
doc_type: "product-docs"
section_path: "Dashboards > Embedded Dashboards > Troubleshooting embedded dashboards"
product_area: "dashboards"
product_version: "4.8"
acl: "enterprise"
updated_at: "2024-03-11"
related_error_codes: ["ERR-1102", "ERR-1147"]
---

# Troubleshooting embedded dashboards

Embedded Dashboards is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When embedded dashboards is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: embedded dashboards performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable embedded dashboards, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

By default, embedded dashboards is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for embedded dashboards are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
