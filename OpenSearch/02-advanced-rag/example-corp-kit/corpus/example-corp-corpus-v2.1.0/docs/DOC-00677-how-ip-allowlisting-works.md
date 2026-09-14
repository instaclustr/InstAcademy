---
source_id: "DOC-00677"
title: "How IP allowlisting works"
doc_type: "product-docs"
section_path: "Data Connectors > Ip Allowlisting > How IP allowlisting works"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2024-06-20"
related_error_codes: ["ERR-2288", "ERR-2209"]
---

# How IP allowlisting works

This page explains how IP allowlisting works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable IP allowlisting, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

By default, IP allowlisting is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for IP allowlisting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, IP allowlisting inherits group membership from your identity provider on each login.

When IP allowlisting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
