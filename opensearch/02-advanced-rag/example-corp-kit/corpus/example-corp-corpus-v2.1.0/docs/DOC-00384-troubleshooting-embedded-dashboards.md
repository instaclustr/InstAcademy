---
source_id: "DOC-00384"
title: "Troubleshooting embedded dashboards"
doc_type: "product-docs"
section_path: "Dashboards > Embedded Dashboards > Troubleshooting embedded dashboards"
product_area: "dashboards"
product_version: "5.1"
acl: "public"
updated_at: "2024-01-13"
related_error_codes: ["ERR-1102", "ERR-1147"]
---

# Troubleshooting embedded dashboards

Embedded Dashboards lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

By default, embedded dashboards is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, embedded dashboards inherits group membership from your identity provider on each login.

Audit events for embedded dashboards are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When embedded dashboards is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: embedded dashboards performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
