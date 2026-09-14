---
source_id: "DOC-00707"
title: "Cross-Filtering overview"
doc_type: "product-docs"
section_path: "Dashboards > Cross-Filtering > Cross-Filtering overview"
product_area: "dashboards"
product_version: "5.0"
acl: "enterprise"
updated_at: "2025-12-18"
related_error_codes: ["ERR-1102", "ERR-1147"]
---

# Cross-Filtering overview

Cross-Filtering is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, cross-filtering inherits group membership from your identity provider on each login.

Audit events for cross-filtering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When cross-filtering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable cross-filtering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

By default, cross-filtering is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
