---
source_id: "DOC-00516"
title: "Usage Analytics overview"
doc_type: "product-docs"
section_path: "Administration > Usage Analytics > Usage Analytics overview"
product_area: "admin"
product_version: "5.1"
acl: "public"
updated_at: "2025-03-10"
related_error_codes: ["ERR-7719", "ERR-7733"]
---

# Usage Analytics overview

This page explains how usage analytics works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable usage analytics, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for usage analytics are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, usage analytics inherits group membership from your identity provider on each login.

By default, usage analytics is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: usage analytics performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
