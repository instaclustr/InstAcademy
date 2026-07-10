---
source_id: "DOC-00513"
title: "Scim Provisioning overview"
doc_type: "product-docs"
section_path: "Administration > Scim Provisioning > Scim Provisioning overview"
product_area: "admin"
product_version: "5.1"
acl: "public"
updated_at: "2025-08-21"
related_error_codes: ["ERR-7733"]
---

# Scim Provisioning overview

This page explains how SCIM provisioning works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, SCIM provisioning inherits group membership from your identity provider on each login.

To enable SCIM provisioning, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for SCIM provisioning are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, SCIM provisioning is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: SCIM provisioning performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
