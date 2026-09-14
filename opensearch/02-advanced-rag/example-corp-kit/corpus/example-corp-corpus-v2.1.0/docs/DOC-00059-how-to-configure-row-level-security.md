---
source_id: "DOC-00059"
title: "How to configure row-level security"
doc_type: "product-docs"
section_path: "Datasets > Row-Level Security > How to configure row-level security"
product_area: "datasets"
product_version: "5.1"
acl: "public"
updated_at: "2026-03-21"
related_error_codes: ["ERR-3305"]
---

# How to configure row-level security

Row-Level Security is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for row-level security are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, row-level security is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: row-level security performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, row-level security inherits group membership from your identity provider on each login.

To enable row-level security, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
