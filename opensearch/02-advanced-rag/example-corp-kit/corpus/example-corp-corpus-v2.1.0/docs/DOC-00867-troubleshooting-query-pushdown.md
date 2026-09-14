---
source_id: "DOC-00867"
title: "Troubleshooting query pushdown"
doc_type: "product-docs"
section_path: "Data Connectors > Query Pushdown > Troubleshooting query pushdown"
product_area: "connectors"
product_version: "4.8"
acl: "professional"
updated_at: "2025-01-11"
related_error_codes: ["ERR-2231"]
---

# Troubleshooting query pushdown

Query Pushdown lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

Audit events for query pushdown are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, query pushdown is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: query pushdown performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, query pushdown inherits group membership from your identity provider on each login.

To enable query pushdown, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
