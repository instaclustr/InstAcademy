---
source_id: "DOC-00856"
title: "Troubleshooting incremental refresh"
doc_type: "product-docs"
section_path: "Datasets > Incremental Refresh > Troubleshooting incremental refresh"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2024-08-19"
related_error_codes: ["ERR-3305"]
---

# Troubleshooting incremental refresh

Incremental Refresh is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, incremental refresh inherits group membership from your identity provider on each login.

By default, incremental refresh is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: incremental refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable incremental refresh, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

When incremental refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
