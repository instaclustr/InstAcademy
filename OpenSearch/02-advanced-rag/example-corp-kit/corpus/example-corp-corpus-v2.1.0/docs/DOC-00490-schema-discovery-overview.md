---
source_id: "DOC-00490"
title: "Schema Discovery overview"
doc_type: "product-docs"
section_path: "Data Connectors > Schema Discovery > Schema Discovery overview"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2024-03-25"
related_error_codes: ["ERR-2288"]
---

# Schema Discovery overview

Schema Discovery lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

To enable schema discovery, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

By default, schema discovery is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, schema discovery inherits group membership from your identity provider on each login.

Performance tip: schema discovery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for schema discovery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
