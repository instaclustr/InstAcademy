---
source_id: "DOC-00151"
title: "Troubleshooting incremental refresh"
doc_type: "product-docs"
section_path: "Datasets > Incremental Refresh > Troubleshooting incremental refresh"
product_area: "datasets"
product_version: "4.8"
acl: "professional"
updated_at: "2025-07-19"
related_error_codes: ["ERR-3340", "ERR-3305"]
---

# Troubleshooting incremental refresh

Incremental Refresh is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, incremental refresh inherits group membership from your identity provider on each login.

To enable incremental refresh, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: incremental refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When incremental refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for incremental refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
