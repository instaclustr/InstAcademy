---
source_id: "DOC-00936"
title: "How SCIM provisioning works"
doc_type: "product-docs"
section_path: "Administration > Scim Provisioning > How SCIM provisioning works"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2024-04-17"
related_error_codes: ["ERR-7719"]
---

# How SCIM provisioning works

This page explains how SCIM provisioning works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable SCIM provisioning, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: SCIM provisioning performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, SCIM provisioning is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When SCIM provisioning is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, SCIM provisioning inherits group membership from your identity provider on each login.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
