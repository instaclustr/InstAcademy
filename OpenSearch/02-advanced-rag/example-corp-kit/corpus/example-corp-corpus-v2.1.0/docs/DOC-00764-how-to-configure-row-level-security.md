---
source_id: "DOC-00764"
title: "How to configure row-level security"
doc_type: "product-docs"
section_path: "Datasets > Row-Level Security > How to configure row-level security"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2024-10-05"
related_error_codes: ["ERR-3305"]
---

# How to configure row-level security

Row-Level Security lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, row-level security inherits group membership from your identity provider on each login.

By default, row-level security is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When row-level security is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: row-level security performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for row-level security are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
