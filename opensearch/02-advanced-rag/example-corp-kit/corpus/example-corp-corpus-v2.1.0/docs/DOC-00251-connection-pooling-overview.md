---
source_id: "DOC-00251"
title: "Connection Pooling overview"
doc_type: "product-docs"
section_path: "Data Connectors > Connection Pooling > Connection Pooling overview"
product_area: "connectors"
product_version: "5.0"
acl: "standard"
updated_at: "2025-11-01"
related_error_codes: ["ERR-2231"]
---

# Connection Pooling overview

This page explains how connection pooling works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, connection pooling inherits group membership from your identity provider on each login.

When connection pooling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: connection pooling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable connection pooling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

By default, connection pooling is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
