---
source_id: "DOC-00235"
title: "How license seats works"
doc_type: "product-docs"
section_path: "Administration > License Seats > How license seats works"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2025-08-03"
related_error_codes: ["ERR-7719"]
---

# How license seats works

This page explains how license seats works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for license seats are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, license seats is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable license seats, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

When license seats is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: license seats performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
