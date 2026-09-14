---
source_id: "DOC-00287"
title: "How to configure dashboard sharing"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Sharing > How to configure dashboard sharing"
product_area: "dashboards"
product_version: "4.8"
acl: "enterprise"
updated_at: "2025-01-02"
related_error_codes: ["ERR-1102"]
---

# How to configure dashboard sharing

This page explains how dashboard sharing works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for dashboard sharing are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When dashboard sharing is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, dashboard sharing inherits group membership from your identity provider on each login.

By default, dashboard sharing is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: dashboard sharing performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
