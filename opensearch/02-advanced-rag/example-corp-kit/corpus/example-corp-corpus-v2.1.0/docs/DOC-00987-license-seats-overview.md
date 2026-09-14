---
source_id: "DOC-00987"
title: "License Seats overview"
doc_type: "product-docs"
section_path: "Administration > License Seats > License Seats overview"
product_area: "admin"
product_version: "4.8"
acl: "public"
updated_at: "2025-01-04"
related_error_codes: ["ERR-7733"]
---

# License Seats overview

This page explains how license seats works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable license seats, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

By default, license seats is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for license seats are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When license seats is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, license seats inherits group membership from your identity provider on each login.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
