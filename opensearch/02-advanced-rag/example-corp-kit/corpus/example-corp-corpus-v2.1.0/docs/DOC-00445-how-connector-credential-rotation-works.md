---
source_id: "DOC-00445"
title: "How connector credential rotation works"
doc_type: "product-docs"
section_path: "Data Connectors > Connector Credential Rotation > How connector credential rotation works"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2024-12-14"
related_error_codes: ["ERR-2209"]
---

# How connector credential rotation works

Connector Credential Rotation is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, connector credential rotation is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When connector credential rotation is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: connector credential rotation performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for connector credential rotation are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, connector credential rotation inherits group membership from your identity provider on each login.

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
