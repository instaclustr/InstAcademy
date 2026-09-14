---
source_id: "DOC-00007"
title: "Mobile Layouts overview"
doc_type: "product-docs"
section_path: "Dashboards > Mobile Layouts > Mobile Layouts overview"
product_area: "dashboards"
product_version: "5.0"
acl: "enterprise"
updated_at: "2024-05-04"
related_error_codes: ["ERR-1102"]
---

# Mobile Layouts overview

This page explains how mobile layouts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When mobile layouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: mobile layouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, mobile layouts is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for mobile layouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable mobile layouts, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
