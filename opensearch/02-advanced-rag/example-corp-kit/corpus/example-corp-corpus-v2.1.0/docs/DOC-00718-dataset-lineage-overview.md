---
source_id: "DOC-00718"
title: "Dataset Lineage overview"
doc_type: "product-docs"
section_path: "Datasets > Dataset Lineage > Dataset Lineage overview"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2024-01-20"
related_error_codes: ["ERR-3305"]
---

# Dataset Lineage overview

Dataset Lineage is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for dataset lineage are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, dataset lineage is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When dataset lineage is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: dataset lineage performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, dataset lineage inherits group membership from your identity provider on each login.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
