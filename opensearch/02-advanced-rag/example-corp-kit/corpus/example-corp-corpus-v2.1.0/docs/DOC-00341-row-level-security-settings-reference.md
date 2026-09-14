---
source_id: "DOC-00341"
title: "Row-Level Security settings reference"
doc_type: "product-docs"
section_path: "Datasets > Row-Level Security > Row-Level Security settings reference"
product_area: "datasets"
product_version: "5.0"
acl: "standard"
updated_at: "2024-07-03"
related_error_codes: ["ERR-3340"]
---

# Row-Level Security settings reference

This page explains how row-level security works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When row-level security is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable row-level security, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, row-level security inherits group membership from your identity provider on each login.

Audit events for row-level security are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: row-level security performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
