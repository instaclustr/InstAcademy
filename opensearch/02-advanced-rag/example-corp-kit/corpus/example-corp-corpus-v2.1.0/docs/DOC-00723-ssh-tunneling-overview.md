---
source_id: "DOC-00723"
title: "Ssh Tunneling overview"
doc_type: "product-docs"
section_path: "Data Connectors > Ssh Tunneling > Ssh Tunneling overview"
product_area: "connectors"
product_version: "4.9"
acl: "public"
updated_at: "2024-09-04"
related_error_codes: ["ERR-2209"]
---

# Ssh Tunneling overview

This page explains how SSH tunneling works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, SSH tunneling is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable SSH tunneling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, SSH tunneling inherits group membership from your identity provider on each login.

Performance tip: SSH tunneling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When SSH tunneling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
