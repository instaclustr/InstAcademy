---
source_id: "DOC-00528"
title: "How to configure calculated fields"
doc_type: "product-docs"
section_path: "Datasets > Calculated Fields > How to configure calculated fields"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2025-09-26"
related_error_codes: ["ERR-3305", "ERR-3340"]
---

# How to configure calculated fields

Calculated Fields lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

Performance tip: calculated fields performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for calculated fields are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, calculated fields is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When calculated fields is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, calculated fields inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
