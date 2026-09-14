---
source_id: "DOC-00765"
title: "How to configure dataset lineage"
doc_type: "product-docs"
section_path: "Datasets > Dataset Lineage > How to configure dataset lineage"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2025-05-01"
related_error_codes: ["ERR-3305"]
---

# How to configure dataset lineage

This page explains how dataset lineage works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, dataset lineage inherits group membership from your identity provider on each login.

By default, dataset lineage is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When dataset lineage is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: dataset lineage performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for dataset lineage are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
