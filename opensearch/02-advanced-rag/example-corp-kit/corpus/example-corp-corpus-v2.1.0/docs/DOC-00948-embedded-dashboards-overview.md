---
source_id: "DOC-00948"
title: "Embedded Dashboards overview"
doc_type: "product-docs"
section_path: "Dashboards > Embedded Dashboards > Embedded Dashboards overview"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2026-03-29"
related_error_codes: ["ERR-1147", "ERR-1102"]
---

# Embedded Dashboards overview

Embedded Dashboards is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, embedded dashboards is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, embedded dashboards inherits group membership from your identity provider on each login.

When embedded dashboards is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable embedded dashboards, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for embedded dashboards are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
