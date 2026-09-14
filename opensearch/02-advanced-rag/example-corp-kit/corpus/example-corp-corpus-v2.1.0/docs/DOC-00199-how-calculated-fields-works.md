---
source_id: "DOC-00199"
title: "How calculated fields works"
doc_type: "product-docs"
section_path: "Datasets > Calculated Fields > How calculated fields works"
product_area: "datasets"
product_version: "5.1"
acl: "public"
updated_at: "2026-01-18"
related_error_codes: ["ERR-3340", "ERR-3305"]
---

# How calculated fields works

Calculated Fields is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, calculated fields inherits group membership from your identity provider on each login.

By default, calculated fields is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: calculated fields performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for calculated fields are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable calculated fields, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
