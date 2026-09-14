---
source_id: "DOC-00962"
title: "Connector Credential Rotation overview"
doc_type: "product-docs"
section_path: "Data Connectors > Connector Credential Rotation > Connector Credential Rotation overview"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2025-12-15"
related_error_codes: ["ERR-2209"]
---

# Connector Credential Rotation overview

Connector Credential Rotation lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, connector credential rotation inherits group membership from your identity provider on each login.

To enable connector credential rotation, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for connector credential rotation are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, connector credential rotation is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: connector credential rotation performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
