---
source_id: "DOC-00576"
title: "Row-Level Security settings reference"
doc_type: "product-docs"
section_path: "Datasets > Row-Level Security > Row-Level Security settings reference"
product_area: "datasets"
product_version: "5.1"
acl: "public"
updated_at: "2026-06-19"
related_error_codes: ["ERR-3305"]
---

# Row-Level Security settings reference

Row-Level Security is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: row-level security performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, row-level security inherits group membership from your identity provider on each login.

To enable row-level security, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

By default, row-level security is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When row-level security is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
