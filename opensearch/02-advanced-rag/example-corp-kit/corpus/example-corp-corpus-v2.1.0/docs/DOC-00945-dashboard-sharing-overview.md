---
source_id: "DOC-00945"
title: "Dashboard Sharing overview"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Sharing > Dashboard Sharing overview"
product_area: "dashboards"
product_version: "4.9"
acl: "standard"
updated_at: "2026-02-14"
related_error_codes: ["ERR-1147"]
---

# Dashboard Sharing overview

Dashboard Sharing lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

By default, dashboard sharing is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable dashboard sharing, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, dashboard sharing inherits group membership from your identity provider on each login.

Audit events for dashboard sharing are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When dashboard sharing is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
