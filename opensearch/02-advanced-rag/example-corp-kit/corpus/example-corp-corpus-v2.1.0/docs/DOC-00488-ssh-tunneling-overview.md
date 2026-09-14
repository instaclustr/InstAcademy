---
source_id: "DOC-00488"
title: "Ssh Tunneling overview"
doc_type: "product-docs"
section_path: "Data Connectors > Ssh Tunneling > Ssh Tunneling overview"
product_area: "connectors"
product_version: "5.1"
acl: "enterprise"
updated_at: "2024-09-19"
related_error_codes: ["ERR-2231"]
---

# Ssh Tunneling overview

This page explains how SSH tunneling works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, SSH tunneling is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, SSH tunneling inherits group membership from your identity provider on each login.

When SSH tunneling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable SSH tunneling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: SSH tunneling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
