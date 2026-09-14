---
source_id: "DOC-00342"
title: "Dataset Lineage settings reference"
doc_type: "product-docs"
section_path: "Datasets > Dataset Lineage > Dataset Lineage settings reference"
product_area: "datasets"
product_version: "4.8"
acl: "public"
updated_at: "2025-12-19"
related_error_codes: ["ERR-3340"]
---

# Dataset Lineage settings reference

Dataset Lineage lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

By default, dataset lineage is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable dataset lineage, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: dataset lineage performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, dataset lineage inherits group membership from your identity provider on each login.

Audit events for dataset lineage are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
