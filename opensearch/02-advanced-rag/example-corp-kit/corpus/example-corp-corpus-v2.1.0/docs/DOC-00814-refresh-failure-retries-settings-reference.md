---
source_id: "DOC-00814"
title: "Refresh Failure Retries settings reference"
doc_type: "product-docs"
section_path: "Datasets > Refresh Failure Retries > Refresh Failure Retries settings reference"
product_area: "datasets"
product_version: "5.1"
acl: "enterprise"
updated_at: "2026-02-27"
related_error_codes: ["ERR-3340"]
---

# Refresh Failure Retries settings reference

This page explains how refresh failure retries works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable refresh failure retries, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: refresh failure retries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, refresh failure retries is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, refresh failure retries inherits group membership from your identity provider on each login.

Audit events for refresh failure retries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
