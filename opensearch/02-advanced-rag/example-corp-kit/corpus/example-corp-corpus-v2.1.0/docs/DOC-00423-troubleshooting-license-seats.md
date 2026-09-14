---
source_id: "DOC-00423"
title: "Troubleshooting license seats"
doc_type: "product-docs"
section_path: "Administration > License Seats > Troubleshooting license seats"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2026-02-20"
related_error_codes: ["ERR-7719", "ERR-7733"]
---

# Troubleshooting license seats

This page explains how license seats works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, license seats inherits group membership from your identity provider on each login.

To enable license seats, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

When license seats is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for license seats are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: license seats performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
