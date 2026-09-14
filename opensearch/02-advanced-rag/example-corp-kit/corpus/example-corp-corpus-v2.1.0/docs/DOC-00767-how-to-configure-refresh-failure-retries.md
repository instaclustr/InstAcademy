---
source_id: "DOC-00767"
title: "How to configure refresh failure retries"
doc_type: "product-docs"
section_path: "Datasets > Refresh Failure Retries > How to configure refresh failure retries"
product_area: "datasets"
product_version: "4.8"
acl: "professional"
updated_at: "2025-01-26"
related_error_codes: ["ERR-3340"]
---

# How to configure refresh failure retries

Refresh Failure Retries is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, refresh failure retries is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for refresh failure retries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable refresh failure retries, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, refresh failure retries inherits group membership from your identity provider on each login.

Performance tip: refresh failure retries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
