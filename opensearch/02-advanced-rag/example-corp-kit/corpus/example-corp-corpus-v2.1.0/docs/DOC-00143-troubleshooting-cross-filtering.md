---
source_id: "DOC-00143"
title: "Troubleshooting cross-filtering"
doc_type: "product-docs"
section_path: "Dashboards > Cross-Filtering > Troubleshooting cross-filtering"
product_area: "dashboards"
product_version: "4.9"
acl: "standard"
updated_at: "2024-09-23"
related_error_codes: ["ERR-1102"]
---

# Troubleshooting cross-filtering

Cross-Filtering lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, cross-filtering inherits group membership from your identity provider on each login.

When cross-filtering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: cross-filtering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for cross-filtering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, cross-filtering is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
