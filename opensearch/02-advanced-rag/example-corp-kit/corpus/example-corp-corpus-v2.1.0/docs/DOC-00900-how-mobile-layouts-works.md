---
source_id: "DOC-00900"
title: "How mobile layouts works"
doc_type: "product-docs"
section_path: "Dashboards > Mobile Layouts > How mobile layouts works"
product_area: "dashboards"
product_version: "4.8"
acl: "public"
updated_at: "2026-02-20"
related_error_codes: ["ERR-1102"]
---

# How mobile layouts works

Mobile Layouts is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable mobile layouts, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

When mobile layouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, mobile layouts is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, mobile layouts inherits group membership from your identity provider on each login.

Audit events for mobile layouts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
