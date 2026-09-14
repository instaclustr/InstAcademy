---
source_id: "DOC-00106"
title: "Row-Level Security settings reference"
doc_type: "product-docs"
section_path: "Datasets > Row-Level Security > Row-Level Security settings reference"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2025-07-28"
related_error_codes: ["ERR-3305"]
---

# Row-Level Security settings reference

This page explains how row-level security works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, row-level security is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: row-level security performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When row-level security is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, row-level security inherits group membership from your identity provider on each login.

Audit events for row-level security are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
