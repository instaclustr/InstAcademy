---
source_id: "DOC-00210"
title: "How connector credential rotation works"
doc_type: "product-docs"
section_path: "Data Connectors > Connector Credential Rotation > How connector credential rotation works"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2024-03-09"
related_error_codes: ["ERR-2209"]
---

# How connector credential rotation works

This page explains how connector credential rotation works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: connector credential rotation performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable connector credential rotation, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for connector credential rotation are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, connector credential rotation is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, connector credential rotation inherits group membership from your identity provider on each login.

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
