---
source_id: "DOC-00379"
title: "Troubleshooting drill-down"
doc_type: "product-docs"
section_path: "Dashboards > Drill-Down > Troubleshooting drill-down"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2026-02-20"
related_error_codes: ["ERR-1102"]
---

# Troubleshooting drill-down

Drill-Down is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for drill-down are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When drill-down is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, drill-down inherits group membership from your identity provider on each login.

Performance tip: drill-down performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable drill-down, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
