---
source_id: "DOC-00532"
title: "How to configure refresh failure retries"
doc_type: "product-docs"
section_path: "Datasets > Refresh Failure Retries > How to configure refresh failure retries"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2024-07-15"
related_error_codes: ["ERR-3305"]
---

# How to configure refresh failure retries

Refresh Failure Retries is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable refresh failure retries, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, refresh failure retries inherits group membership from your identity provider on each login.

Performance tip: refresh failure retries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for refresh failure retries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, refresh failure retries is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
