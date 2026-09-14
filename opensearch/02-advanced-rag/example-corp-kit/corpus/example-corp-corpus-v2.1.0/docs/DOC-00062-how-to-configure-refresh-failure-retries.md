---
source_id: "DOC-00062"
title: "How to configure refresh failure retries"
doc_type: "product-docs"
section_path: "Datasets > Refresh Failure Retries > How to configure refresh failure retries"
product_area: "datasets"
product_version: "4.8"
acl: "standard"
updated_at: "2024-05-27"
related_error_codes: ["ERR-3340", "ERR-3305"]
---

# How to configure refresh failure retries

Refresh Failure Retries lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

Performance tip: refresh failure retries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, refresh failure retries inherits group membership from your identity provider on each login.

When refresh failure retries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable refresh failure retries, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

By default, refresh failure retries is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
