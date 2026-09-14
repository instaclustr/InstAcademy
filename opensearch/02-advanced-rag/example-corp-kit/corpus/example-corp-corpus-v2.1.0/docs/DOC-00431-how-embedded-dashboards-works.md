---
source_id: "DOC-00431"
title: "How embedded dashboards works"
doc_type: "product-docs"
section_path: "Dashboards > Embedded Dashboards > How embedded dashboards works"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2024-04-02"
related_error_codes: ["ERR-1147"]
---

# How embedded dashboards works

Embedded Dashboards lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

By default, embedded dashboards is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for embedded dashboards are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, embedded dashboards inherits group membership from your identity provider on each login.

When embedded dashboards is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable embedded dashboards, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
