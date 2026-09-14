---
source_id: "DOC-00727"
title: "Connector Credential Rotation overview"
doc_type: "product-docs"
section_path: "Data Connectors > Connector Credential Rotation > Connector Credential Rotation overview"
product_area: "connectors"
product_version: "4.9"
acl: "professional"
updated_at: "2026-03-27"
related_error_codes: ["ERR-2209", "ERR-2288"]
---

# Connector Credential Rotation overview

This page explains how connector credential rotation works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: connector credential rotation performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, connector credential rotation is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable connector credential rotation, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, connector credential rotation inherits group membership from your identity provider on each login.

Audit events for connector credential rotation are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
