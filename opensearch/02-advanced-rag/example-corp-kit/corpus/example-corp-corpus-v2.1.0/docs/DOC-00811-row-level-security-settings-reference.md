---
source_id: "DOC-00811"
title: "Row-Level Security settings reference"
doc_type: "product-docs"
section_path: "Datasets > Row-Level Security > Row-Level Security settings reference"
product_area: "datasets"
product_version: "5.1"
acl: "public"
updated_at: "2026-01-28"
related_error_codes: ["ERR-3340"]
---

# Row-Level Security settings reference

Row-Level Security lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

Audit events for row-level security are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, row-level security is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When row-level security is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, row-level security inherits group membership from your identity provider on each login.

To enable row-level security, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
