---
source_id: "DOC-00014"
title: "Materialized Views overview"
doc_type: "product-docs"
section_path: "Datasets > Materialized Views > Materialized Views overview"
product_area: "datasets"
product_version: "4.9"
acl: "standard"
updated_at: "2026-05-03"
related_error_codes: ["ERR-3340", "ERR-3305"]
---

# Materialized Views overview

Materialized Views lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

To enable materialized views, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for materialized views are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, materialized views inherits group membership from your identity provider on each login.

When materialized views is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: materialized views performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
