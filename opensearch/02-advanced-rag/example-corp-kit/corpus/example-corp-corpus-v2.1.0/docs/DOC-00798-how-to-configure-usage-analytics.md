---
source_id: "DOC-00798"
title: "How to configure usage analytics"
doc_type: "product-docs"
section_path: "Administration > Usage Analytics > How to configure usage analytics"
product_area: "admin"
product_version: "5.1"
acl: "public"
updated_at: "2024-11-24"
related_error_codes: ["ERR-7719"]
---

# How to configure usage analytics

Usage Analytics is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for usage analytics are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, usage analytics is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable usage analytics, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

When usage analytics is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: usage analytics performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
