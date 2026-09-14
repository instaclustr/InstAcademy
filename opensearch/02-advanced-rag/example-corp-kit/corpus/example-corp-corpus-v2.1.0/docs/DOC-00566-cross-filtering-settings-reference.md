---
source_id: "DOC-00566"
title: "Cross-Filtering settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Cross-Filtering > Cross-Filtering settings reference"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2026-05-16"
related_error_codes: ["ERR-1102"]
---

# Cross-Filtering settings reference

Cross-Filtering is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, cross-filtering inherits group membership from your identity provider on each login.

Audit events for cross-filtering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: cross-filtering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable cross-filtering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When cross-filtering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
