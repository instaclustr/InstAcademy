---
source_id: "DOC-00623"
title: "Troubleshooting row-level security"
doc_type: "product-docs"
section_path: "Datasets > Row-Level Security > Troubleshooting row-level security"
product_area: "datasets"
product_version: "4.8"
acl: "public"
updated_at: "2024-11-18"
related_error_codes: ["ERR-3305"]
---

# Troubleshooting row-level security

Row-Level Security lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

When row-level security is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for row-level security are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: row-level security performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, row-level security is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable row-level security, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
