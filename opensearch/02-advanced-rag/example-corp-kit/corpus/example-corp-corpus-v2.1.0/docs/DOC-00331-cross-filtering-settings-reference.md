---
source_id: "DOC-00331"
title: "Cross-Filtering settings reference"
doc_type: "product-docs"
section_path: "Dashboards > Cross-Filtering > Cross-Filtering settings reference"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2025-10-22"
related_error_codes: ["ERR-1210", "ERR-1147"]
---

# Cross-Filtering settings reference

This page explains how cross-filtering works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for cross-filtering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: cross-filtering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, cross-filtering inherits group membership from your identity provider on each login.

When cross-filtering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable cross-filtering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
