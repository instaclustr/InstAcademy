---
source_id: "DOC-00056"
title: "How to configure dataset refresh scheduling"
doc_type: "product-docs"
section_path: "Datasets > Dataset Refresh Scheduling > How to configure dataset refresh scheduling"
product_area: "datasets"
product_version: "4.8"
acl: "public"
updated_at: "2024-08-21"
related_error_codes: ["ERR-3305"]
---

# How to configure dataset refresh scheduling

Dataset Refresh Scheduling is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for dataset refresh scheduling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable dataset refresh scheduling, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, dataset refresh scheduling inherits group membership from your identity provider on each login.

By default, dataset refresh scheduling is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: dataset refresh scheduling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
