---
source_id: "DOC-00441"
title: "How SSH tunneling works"
doc_type: "product-docs"
section_path: "Data Connectors > Ssh Tunneling > How SSH tunneling works"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2025-06-07"
related_error_codes: ["ERR-2231"]
---

# How SSH tunneling works

This page explains how SSH tunneling works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When SSH tunneling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, SSH tunneling is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable SSH tunneling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for SSH tunneling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, SSH tunneling inherits group membership from your identity provider on each login.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
