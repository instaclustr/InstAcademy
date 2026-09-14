---
source_id: "DOC-00107"
title: "Dataset Lineage settings reference"
doc_type: "product-docs"
section_path: "Datasets > Dataset Lineage > Dataset Lineage settings reference"
product_area: "datasets"
product_version: "4.8"
acl: "public"
updated_at: "2024-05-09"
related_error_codes: ["ERR-3340"]
---

# Dataset Lineage settings reference

This page explains how dataset lineage works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, dataset lineage inherits group membership from your identity provider on each login.

By default, dataset lineage is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable dataset lineage, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

When dataset lineage is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: dataset lineage performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
