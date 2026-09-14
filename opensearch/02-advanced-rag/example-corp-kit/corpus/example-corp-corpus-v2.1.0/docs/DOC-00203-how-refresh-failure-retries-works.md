---
source_id: "DOC-00203"
title: "How refresh failure retries works"
doc_type: "product-docs"
section_path: "Datasets > Refresh Failure Retries > How refresh failure retries works"
product_area: "datasets"
product_version: "4.9"
acl: "professional"
updated_at: "2024-11-20"
related_error_codes: ["ERR-3305", "ERR-3340"]
---

# How refresh failure retries works

Refresh Failure Retries lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, refresh failure retries inherits group membership from your identity provider on each login.

Audit events for refresh failure retries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable refresh failure retries, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

When refresh failure retries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: refresh failure retries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
