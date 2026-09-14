---
source_id: "DOC-00288"
title: "How to configure PDF export"
doc_type: "product-docs"
section_path: "Dashboards > Pdf Export > How to configure PDF export"
product_area: "dashboards"
product_version: "5.1"
acl: "standard"
updated_at: "2026-03-22"
related_error_codes: ["ERR-1102"]
---

# How to configure PDF export

Pdf Export lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Performance tip: PDF export performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When PDF export is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, PDF export is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for PDF export are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, PDF export inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
