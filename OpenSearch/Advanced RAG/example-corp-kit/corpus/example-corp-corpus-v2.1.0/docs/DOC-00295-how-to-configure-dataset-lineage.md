---
source_id: "DOC-00295"
title: "How to configure dataset lineage"
doc_type: "product-docs"
section_path: "Datasets > Dataset Lineage > How to configure dataset lineage"
product_area: "datasets"
product_version: "5.0"
acl: "enterprise"
updated_at: "2026-02-27"
related_error_codes: ["ERR-3305"]
---

# How to configure dataset lineage

Dataset Lineage is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, dataset lineage is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When dataset lineage is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, dataset lineage inherits group membership from your identity provider on each login.

To enable dataset lineage, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for dataset lineage are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
