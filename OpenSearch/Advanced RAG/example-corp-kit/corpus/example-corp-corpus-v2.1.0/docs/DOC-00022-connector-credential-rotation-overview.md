---
source_id: "DOC-00022"
title: "Connector Credential Rotation overview"
doc_type: "product-docs"
section_path: "Data Connectors > Connector Credential Rotation > Connector Credential Rotation overview"
product_area: "connectors"
product_version: "5.0"
acl: "public"
updated_at: "2025-01-27"
related_error_codes: ["ERR-2231"]
---

# Connector Credential Rotation overview

Connector Credential Rotation is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When connector credential rotation is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: connector credential rotation performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, connector credential rotation inherits group membership from your identity provider on each login.

Audit events for connector credential rotation are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable connector credential rotation, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
