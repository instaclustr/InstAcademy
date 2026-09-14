---
source_id: "DOC-00704"
title: "How usage analytics works"
doc_type: "product-docs"
section_path: "Administration > Usage Analytics > How usage analytics works"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2025-02-06"
related_error_codes: ["ERR-7733", "ERR-7719"]
---

# How usage analytics works

This page explains how usage analytics works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable usage analytics, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: usage analytics performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, usage analytics inherits group membership from your identity provider on each login.

When usage analytics is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for usage analytics are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
