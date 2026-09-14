---
source_id: "DOC-00109"
title: "Refresh Failure Retries settings reference"
doc_type: "product-docs"
section_path: "Datasets > Refresh Failure Retries > Refresh Failure Retries settings reference"
product_area: "datasets"
product_version: "4.8"
acl: "public"
updated_at: "2025-05-11"
related_error_codes: ["ERR-3305"]
---

# Refresh Failure Retries settings reference

This page explains how refresh failure retries works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: refresh failure retries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable refresh failure retries, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for refresh failure retries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When refresh failure retries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, refresh failure retries inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
