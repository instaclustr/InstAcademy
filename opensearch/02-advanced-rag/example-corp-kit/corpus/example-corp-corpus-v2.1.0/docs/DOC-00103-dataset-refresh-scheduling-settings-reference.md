---
source_id: "DOC-00103"
title: "Dataset Refresh Scheduling settings reference"
doc_type: "product-docs"
section_path: "Datasets > Dataset Refresh Scheduling > Dataset Refresh Scheduling settings reference"
product_area: "datasets"
product_version: "5.1"
acl: "standard"
updated_at: "2026-05-02"
related_error_codes: ["ERR-3305"]
---

# Dataset Refresh Scheduling settings reference

This page explains how dataset refresh scheduling works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for dataset refresh scheduling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, dataset refresh scheduling inherits group membership from your identity provider on each login.

By default, dataset refresh scheduling is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: dataset refresh scheduling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable dataset refresh scheduling, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
