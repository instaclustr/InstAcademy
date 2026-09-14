---
source_id: "DOC-00585"
title: "Query Pushdown settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Query Pushdown > Query Pushdown settings reference"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2024-05-17"
related_error_codes: ["ERR-2209"]
---

# Query Pushdown settings reference

This page explains how query pushdown works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, query pushdown is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, query pushdown inherits group membership from your identity provider on each login.

Performance tip: query pushdown performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for query pushdown are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable query pushdown, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
