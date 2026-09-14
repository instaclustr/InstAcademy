---
source_id: "DOC-00953"
title: "Dataset Lineage overview"
doc_type: "product-docs"
section_path: "Datasets > Dataset Lineage > Dataset Lineage overview"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2026-01-14"
related_error_codes: ["ERR-3305"]
---

# Dataset Lineage overview

This page explains how dataset lineage works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, dataset lineage is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, dataset lineage inherits group membership from your identity provider on each login.

To enable dataset lineage, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for dataset lineage are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: dataset lineage performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
