---
source_id: "DOC-00444"
title: "How query pushdown works"
doc_type: "product-docs"
section_path: "Data Connectors > Query Pushdown > How query pushdown works"
product_area: "connectors"
product_version: "5.0"
acl: "public"
updated_at: "2024-05-26"
related_error_codes: ["ERR-2209", "ERR-2231"]
---

# How query pushdown works

Query Pushdown lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, query pushdown inherits group membership from your identity provider on each login.

By default, query pushdown is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable query pushdown, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: query pushdown performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for query pushdown are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
