---
source_id: "DOC-00343"
title: "Materialized Views settings reference"
doc_type: "product-docs"
section_path: "Datasets > Materialized Views > Materialized Views settings reference"
product_area: "datasets"
product_version: "4.8"
acl: "public"
updated_at: "2025-12-04"
related_error_codes: ["ERR-3340"]
---

# Materialized Views settings reference

Materialized Views lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, materialized views inherits group membership from your identity provider on each login.

Audit events for materialized views are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When materialized views is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: materialized views performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable materialized views, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
