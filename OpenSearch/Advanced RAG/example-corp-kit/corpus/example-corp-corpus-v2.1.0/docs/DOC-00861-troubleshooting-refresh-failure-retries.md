---
source_id: "DOC-00861"
title: "Troubleshooting refresh failure retries"
doc_type: "product-docs"
section_path: "Datasets > Refresh Failure Retries > Troubleshooting refresh failure retries"
product_area: "datasets"
product_version: "5.0"
acl: "public"
updated_at: "2026-02-15"
related_error_codes: ["ERR-3305"]
---

# Troubleshooting refresh failure retries

Refresh Failure Retries is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, refresh failure retries is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for refresh failure retries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: refresh failure retries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable refresh failure retries, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

When refresh failure retries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
