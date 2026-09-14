---
source_id: "DOC-01000"
title: "How to configure dataset lineage"
doc_type: "product-docs"
section_path: "Datasets > Dataset Lineage > How to configure dataset lineage"
product_area: "datasets"
product_version: "4.8"
acl: "public"
updated_at: "2025-06-13"
related_error_codes: ["ERR-3340", "ERR-3305"]
---

# How to configure dataset lineage

Dataset Lineage lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, dataset lineage inherits group membership from your identity provider on each login.

Audit events for dataset lineage are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable dataset lineage, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: dataset lineage performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, dataset lineage is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
