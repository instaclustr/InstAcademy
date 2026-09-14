---
source_id: "DOC-00852"
title: "Troubleshooting PDF export"
doc_type: "product-docs"
section_path: "Dashboards > Pdf Export > Troubleshooting PDF export"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2024-01-17"
related_error_codes: ["ERR-1102"]
---

# Troubleshooting PDF export

Pdf Export lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

Audit events for PDF export are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When PDF export is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: PDF export performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable PDF export, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

By default, PDF export is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
