---
source_id: "DOC-00338"
title: "Dataset Refresh Scheduling settings reference"
doc_type: "product-docs"
section_path: "Datasets > Dataset Refresh Scheduling > Dataset Refresh Scheduling settings reference"
product_area: "datasets"
product_version: "5.0"
acl: "professional"
updated_at: "2026-01-07"
related_error_codes: ["ERR-3340"]
---

# Dataset Refresh Scheduling settings reference

Dataset Refresh Scheduling lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, dataset refresh scheduling inherits group membership from your identity provider on each login.

Audit events for dataset refresh scheduling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: dataset refresh scheduling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, dataset refresh scheduling is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When dataset refresh scheduling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
