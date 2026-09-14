---
source_id: "DOC-00301"
title: "How to configure IP allowlisting"
doc_type: "product-docs"
section_path: "Data Connectors > Ip Allowlisting > How to configure IP allowlisting"
product_area: "connectors"
product_version: "4.9"
acl: "professional"
updated_at: "2025-09-01"
related_error_codes: ["ERR-2288"]
---

# How to configure IP allowlisting

Ip Allowlisting lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Audit events for IP allowlisting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, IP allowlisting is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, IP allowlisting inherits group membership from your identity provider on each login.

To enable IP allowlisting, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: IP allowlisting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
