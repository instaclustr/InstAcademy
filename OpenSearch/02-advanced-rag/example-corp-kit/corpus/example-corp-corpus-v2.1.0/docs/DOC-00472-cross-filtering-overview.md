---
source_id: "DOC-00472"
title: "Cross-Filtering overview"
doc_type: "product-docs"
section_path: "Dashboards > Cross-Filtering > Cross-Filtering overview"
product_area: "dashboards"
product_version: "5.1"
acl: "professional"
updated_at: "2025-02-27"
related_error_codes: ["ERR-1147", "ERR-1102"]
---

# Cross-Filtering overview

Cross-Filtering lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

By default, cross-filtering is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, cross-filtering inherits group membership from your identity provider on each login.

Performance tip: cross-filtering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable cross-filtering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When cross-filtering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
