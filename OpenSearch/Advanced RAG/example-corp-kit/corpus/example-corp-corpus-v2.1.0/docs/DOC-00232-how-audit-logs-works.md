---
source_id: "DOC-00232"
title: "How audit logs works"
doc_type: "product-docs"
section_path: "Administration > Audit Logs > How audit logs works"
product_area: "admin"
product_version: "4.8"
acl: "public"
updated_at: "2025-10-14"
related_error_codes: ["ERR-7719"]
---

# How audit logs works

Audit Logs is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, audit logs is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When audit logs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable audit logs, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for audit logs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: audit logs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
