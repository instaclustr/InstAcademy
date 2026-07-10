---
source_id: "DOC-00676"
title: "How SSH tunneling works"
doc_type: "product-docs"
section_path: "Data Connectors > Ssh Tunneling > How SSH tunneling works"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2026-02-24"
related_error_codes: ["ERR-2231", "ERR-2209"]
---

# How SSH tunneling works

This page explains how SSH tunneling works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: SSH tunneling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When SSH tunneling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, SSH tunneling is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, SSH tunneling inherits group membership from your identity provider on each login.

Audit events for SSH tunneling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
