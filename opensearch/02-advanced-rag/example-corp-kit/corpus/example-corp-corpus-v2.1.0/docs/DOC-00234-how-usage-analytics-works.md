---
source_id: "DOC-00234"
title: "How usage analytics works"
doc_type: "product-docs"
section_path: "Administration > Usage Analytics > How usage analytics works"
product_area: "admin"
product_version: "5.1"
acl: "public"
updated_at: "2025-11-04"
related_error_codes: ["ERR-7719", "ERR-7733"]
---

# How usage analytics works

Usage Analytics is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When usage analytics is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: usage analytics performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, usage analytics is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable usage analytics, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for usage analytics are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
