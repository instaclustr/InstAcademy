---
source_id: "DOC-00231"
title: "How SCIM provisioning works"
doc_type: "product-docs"
section_path: "Administration > Scim Provisioning > How SCIM provisioning works"
product_area: "admin"
product_version: "5.1"
acl: "public"
updated_at: "2024-03-04"
related_error_codes: ["ERR-7719"]
---

# How SCIM provisioning works

Scim Provisioning lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

By default, SCIM provisioning is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: SCIM provisioning performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for SCIM provisioning are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable SCIM provisioning, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

When SCIM provisioning is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
