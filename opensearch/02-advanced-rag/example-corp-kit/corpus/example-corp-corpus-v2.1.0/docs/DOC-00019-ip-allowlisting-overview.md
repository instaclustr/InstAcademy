---
source_id: "DOC-00019"
title: "Ip Allowlisting overview"
doc_type: "product-docs"
section_path: "Data Connectors > Ip Allowlisting > Ip Allowlisting overview"
product_area: "connectors"
product_version: "4.9"
acl: "public"
updated_at: "2024-01-27"
related_error_codes: ["ERR-2209", "ERR-2288"]
---

# Ip Allowlisting overview

Ip Allowlisting lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

To enable IP allowlisting, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

By default, IP allowlisting is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When IP allowlisting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for IP allowlisting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, IP allowlisting inherits group membership from your identity provider on each login.

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
