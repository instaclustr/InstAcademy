---
source_id: "DOC-00378"
title: "Troubleshooting cross-filtering"
doc_type: "product-docs"
section_path: "Dashboards > Cross-Filtering > Troubleshooting cross-filtering"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2026-03-17"
related_error_codes: ["ERR-1102"]
---

# Troubleshooting cross-filtering

Cross-Filtering is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable cross-filtering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for cross-filtering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, cross-filtering is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When cross-filtering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, cross-filtering inherits group membership from your identity provider on each login.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
