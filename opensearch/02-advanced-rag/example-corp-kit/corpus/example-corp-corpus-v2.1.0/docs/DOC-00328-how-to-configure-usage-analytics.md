---
source_id: "DOC-00328"
title: "How to configure usage analytics"
doc_type: "product-docs"
section_path: "Administration > Usage Analytics > How to configure usage analytics"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2025-04-10"
related_error_codes: ["ERR-7733"]
---

# How to configure usage analytics

This page explains how usage analytics works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable usage analytics, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for usage analytics are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, usage analytics is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: usage analytics performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When usage analytics is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
