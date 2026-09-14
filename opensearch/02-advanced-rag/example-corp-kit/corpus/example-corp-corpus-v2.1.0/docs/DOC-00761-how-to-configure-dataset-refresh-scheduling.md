---
source_id: "DOC-00761"
title: "How to configure dataset refresh scheduling"
doc_type: "product-docs"
section_path: "Datasets > Dataset Refresh Scheduling > How to configure dataset refresh scheduling"
product_area: "datasets"
product_version: "5.1"
acl: "standard"
updated_at: "2025-05-04"
related_error_codes: ["ERR-3305"]
---

# How to configure dataset refresh scheduling

Dataset Refresh Scheduling is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable dataset refresh scheduling, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for dataset refresh scheduling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: dataset refresh scheduling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When dataset refresh scheduling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, dataset refresh scheduling inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
