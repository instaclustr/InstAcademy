---
source_id: "DOC-00986"
title: "Usage Analytics overview"
doc_type: "product-docs"
section_path: "Administration > Usage Analytics > Usage Analytics overview"
product_area: "admin"
product_version: "5.1"
acl: "public"
updated_at: "2026-03-01"
related_error_codes: ["ERR-7719"]
---

# Usage Analytics overview

Usage Analytics is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, usage analytics inherits group membership from your identity provider on each login.

Audit events for usage analytics are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: usage analytics performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable usage analytics, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

By default, usage analytics is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
