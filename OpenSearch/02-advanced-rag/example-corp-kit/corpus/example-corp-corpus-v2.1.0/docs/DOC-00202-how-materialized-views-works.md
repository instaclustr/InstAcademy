---
source_id: "DOC-00202"
title: "How materialized views works"
doc_type: "product-docs"
section_path: "Datasets > Materialized Views > How materialized views works"
product_area: "datasets"
product_version: "4.9"
acl: "professional"
updated_at: "2025-06-25"
related_error_codes: ["ERR-3305"]
---

# How materialized views works

Materialized Views is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, materialized views inherits group membership from your identity provider on each login.

By default, materialized views is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: materialized views performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for materialized views are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable materialized views, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
