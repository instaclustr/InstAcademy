---
source_id: "DOC-00100"
title: "Pdf Export settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Pdf Export > Pdf Export settings reference"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2025-01-05"
related_error_codes: ["ERR-1102"]
---

# Pdf Export settings reference

Pdf Export is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable PDF export, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, PDF export inherits group membership from your identity provider on each login.

When PDF export is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, PDF export is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: PDF export performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
