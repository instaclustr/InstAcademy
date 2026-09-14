---
source_id: "DOC-00891"
title: "Troubleshooting workspace permissions"
doc_type: "product-docs"
section_path: "Administration > Workspace Permissions > Troubleshooting workspace permissions"
product_area: "admin"
product_version: "4.8"
acl: "standard"
updated_at: "2025-03-17"
related_error_codes: ["ERR-7733"]
---

# Troubleshooting workspace permissions

This page explains how workspace permissions works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for workspace permissions are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable workspace permissions, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

By default, workspace permissions is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When workspace permissions is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, workspace permissions inherits group membership from your identity provider on each login.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
