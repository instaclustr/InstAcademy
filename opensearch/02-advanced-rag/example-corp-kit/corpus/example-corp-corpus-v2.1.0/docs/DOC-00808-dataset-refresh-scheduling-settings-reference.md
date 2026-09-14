---
source_id: "DOC-00808"
title: "Dataset Refresh Scheduling settings reference"
doc_type: "product-docs"
section_path: "Datasets > Dataset Refresh Scheduling > Dataset Refresh Scheduling settings reference"
product_area: "datasets"
product_version: "5.0"
acl: "public"
updated_at: "2024-12-07"
related_error_codes: ["ERR-3340", "ERR-3305"]
---

# Dataset Refresh Scheduling settings reference

This page explains how dataset refresh scheduling works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When dataset refresh scheduling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for dataset refresh scheduling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: dataset refresh scheduling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, dataset refresh scheduling is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, dataset refresh scheduling inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
