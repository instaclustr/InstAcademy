---
source_id: "DOC-00519"
title: "How to configure cross-filtering"
doc_type: "product-docs"
section_path: "Dashboards > Cross-Filtering > How to configure cross-filtering"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2025-10-20"
related_error_codes: ["ERR-1102"]
---

# How to configure cross-filtering

Cross-Filtering lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

To enable cross-filtering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for cross-filtering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: cross-filtering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, cross-filtering is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, cross-filtering inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
