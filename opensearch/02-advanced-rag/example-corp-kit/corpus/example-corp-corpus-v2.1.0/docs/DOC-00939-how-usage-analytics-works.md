---
source_id: "DOC-00939"
title: "How usage analytics works"
doc_type: "product-docs"
section_path: "Administration > Usage Analytics > How usage analytics works"
product_area: "admin"
product_version: "4.8"
acl: "public"
updated_at: "2025-10-23"
related_error_codes: ["ERR-7719"]
---

# How usage analytics works

Usage Analytics lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

When usage analytics is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for usage analytics are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: usage analytics performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, usage analytics is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, usage analytics inherits group membership from your identity provider on each login.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
