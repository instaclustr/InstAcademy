---
source_id: "DOC-00572"
title: "Embedded Dashboards settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Embedded Dashboards > Embedded Dashboards settings reference"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2024-04-14"
related_error_codes: ["ERR-1102"]
---

# Embedded Dashboards settings reference

Embedded Dashboards lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

By default, embedded dashboards is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When embedded dashboards is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: embedded dashboards performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, embedded dashboards inherits group membership from your identity provider on each login.

To enable embedded dashboards, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
