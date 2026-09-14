---
source_id: "DOC-00044"
title: "Audit Logs overview"
doc_type: "product-docs"
section_path: "Administration > Audit Logs > Audit Logs overview"
product_area: "admin"
product_version: "4.8"
acl: "standard"
updated_at: "2024-08-26"
related_error_codes: ["ERR-7719"]
---

# Audit Logs overview

This page explains how audit logs works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable audit logs, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

By default, audit logs is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When audit logs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: audit logs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for audit logs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
