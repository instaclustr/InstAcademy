---
source_id: "DOC-00052"
title: "How to configure dashboard sharing"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Sharing > How to configure dashboard sharing"
product_area: "dashboards"
product_version: "5.0"
acl: "enterprise"
updated_at: "2024-08-05"
related_error_codes: ["ERR-1102", "ERR-1147"]
---

# How to configure dashboard sharing

Dashboard Sharing is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, dashboard sharing inherits group membership from your identity provider on each login.

To enable dashboard sharing, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for dashboard sharing are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, dashboard sharing is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When dashboard sharing is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
