---
source_id: "DOC-00912"
title: "How IP allowlisting works"
doc_type: "product-docs"
section_path: "Data Connectors > Ip Allowlisting > How IP allowlisting works"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2024-08-16"
related_error_codes: ["ERR-2288"]
---

# How IP allowlisting works

Ip Allowlisting is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for IP allowlisting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, IP allowlisting is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, IP allowlisting inherits group membership from your identity provider on each login.

To enable IP allowlisting, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: IP allowlisting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
