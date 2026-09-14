---
source_id: "DOC-00958"
title: "Ssh Tunneling overview"
doc_type: "product-docs"
section_path: "Data Connectors > Ssh Tunneling > Ssh Tunneling overview"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2025-04-15"
related_error_codes: ["ERR-2288"]
---

# Ssh Tunneling overview

Ssh Tunneling lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, SSH tunneling inherits group membership from your identity provider on each login.

When SSH tunneling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable SSH tunneling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for SSH tunneling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, SSH tunneling is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
