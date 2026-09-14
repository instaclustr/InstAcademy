---
source_id: "DOC-00905"
title: "How row-level security works"
doc_type: "product-docs"
section_path: "Datasets > Row-Level Security > How row-level security works"
product_area: "datasets"
product_version: "5.0"
acl: "public"
updated_at: "2024-10-19"
related_error_codes: ["ERR-3305"]
---

# How row-level security works

Row-Level Security is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for row-level security are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: row-level security performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When row-level security is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable row-level security, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

By default, row-level security is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
