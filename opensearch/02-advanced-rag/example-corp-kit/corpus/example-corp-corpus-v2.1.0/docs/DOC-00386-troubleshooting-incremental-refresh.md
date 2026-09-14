---
source_id: "DOC-00386"
title: "Troubleshooting incremental refresh"
doc_type: "product-docs"
section_path: "Datasets > Incremental Refresh > Troubleshooting incremental refresh"
product_area: "datasets"
product_version: "5.0"
acl: "public"
updated_at: "2024-07-01"
related_error_codes: ["ERR-3340", "ERR-3305"]
---

# Troubleshooting incremental refresh

Incremental Refresh is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: incremental refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, incremental refresh inherits group membership from your identity provider on each login.

Audit events for incremental refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, incremental refresh is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When incremental refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
