---
source_id: "DOC-00278"
title: "Scim Provisioning overview"
doc_type: "product-docs"
section_path: "Administration > Scim Provisioning > Scim Provisioning overview"
product_area: "admin"
product_version: "4.9"
acl: "standard"
updated_at: "2025-03-24"
related_error_codes: ["ERR-7719", "ERR-7733"]
---

# Scim Provisioning overview

This page explains how SCIM provisioning works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for SCIM provisioning are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, SCIM provisioning inherits group membership from your identity provider on each login.

Performance tip: SCIM provisioning performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable SCIM provisioning, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

When SCIM provisioning is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
