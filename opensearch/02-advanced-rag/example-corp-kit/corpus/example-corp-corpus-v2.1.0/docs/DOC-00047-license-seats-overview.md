---
source_id: "DOC-00047"
title: "License Seats overview"
doc_type: "product-docs"
section_path: "Administration > License Seats > License Seats overview"
product_area: "admin"
product_version: "5.1"
acl: "public"
updated_at: "2025-07-12"
related_error_codes: ["ERR-7733"]
---

# License Seats overview

License Seats is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: license seats performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, license seats inherits group membership from your identity provider on each login.

When license seats is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable license seats, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for license seats are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
