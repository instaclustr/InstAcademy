---
source_id: "DOC-00082"
title: "How to configure CSV download limits"
doc_type: "product-docs"
section_path: "SQL Workbench > Csv Download Limits > How to configure CSV download limits"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2025-05-19"
related_error_codes: ["ERR-5501"]
---

# How to configure CSV download limits

Csv Download Limits is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: CSV download limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for CSV download limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable CSV download limits, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, CSV download limits inherits group membership from your identity provider on each login.

By default, CSV download limits is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
