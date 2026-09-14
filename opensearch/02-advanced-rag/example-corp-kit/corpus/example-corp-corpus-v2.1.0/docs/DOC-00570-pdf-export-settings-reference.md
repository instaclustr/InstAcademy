---
source_id: "DOC-00570"
title: "Pdf Export settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Pdf Export > Pdf Export settings reference"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2024-01-22"
related_error_codes: ["ERR-1102", "ERR-1147"]
---

# Pdf Export settings reference

Pdf Export lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

Performance tip: PDF export performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When PDF export is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for PDF export are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, PDF export inherits group membership from your identity provider on each login.

To enable PDF export, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
