---
source_id: "DOC-00520"
title: "How to configure drill-down"
doc_type: "product-docs"
section_path: "Dashboards > Drill-Down > How to configure drill-down"
product_area: "dashboards"
product_version: "4.9"
acl: "enterprise"
updated_at: "2024-03-14"
related_error_codes: ["ERR-1102"]
---

# How to configure drill-down

Drill-Down lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

Audit events for drill-down are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, drill-down inherits group membership from your identity provider on each login.

By default, drill-down is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: drill-down performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When drill-down is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
