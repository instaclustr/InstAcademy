---
source_id: "DOC-00194"
title: "How PDF export works"
doc_type: "product-docs"
section_path: "Dashboards > Pdf Export > How PDF export works"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2025-11-27"
related_error_codes: ["ERR-1147"]
---

# How PDF export works

Pdf Export lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, PDF export inherits group membership from your identity provider on each login.

Audit events for PDF export are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, PDF export is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable PDF export, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When PDF export is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
