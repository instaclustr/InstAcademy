---
source_id: "DOC-00237"
title: "Cross-Filtering overview"
doc_type: "product-docs"
section_path: "Dashboards > Cross-Filtering > Cross-Filtering overview"
product_area: "dashboards"
product_version: "4.9"
acl: "public"
updated_at: "2025-12-30"
related_error_codes: ["ERR-1102"]
---

# Cross-Filtering overview

Cross-Filtering lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

Performance tip: cross-filtering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, cross-filtering is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable cross-filtering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, cross-filtering inherits group membership from your identity provider on each login.

Audit events for cross-filtering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
