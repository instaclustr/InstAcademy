---
source_id: "DOC-00277"
title: "Saml Sso overview"
doc_type: "product-docs"
section_path: "Administration > Saml Sso > Saml Sso overview"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2024-12-09"
related_error_codes: ["ERR-7719"]
---

# Saml Sso overview

This page explains how SAML SSO works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When SAML SSO is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: SAML SSO performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable SAML SSO, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, SAML SSO inherits group membership from your identity provider on each login.

Audit events for SAML SSO are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
