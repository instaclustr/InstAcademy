---
source_id: "DOC-00955"
title: "Refresh Failure Retries overview"
doc_type: "product-docs"
section_path: "Datasets > Refresh Failure Retries > Refresh Failure Retries overview"
product_area: "datasets"
product_version: "4.9"
acl: "enterprise"
updated_at: "2024-04-15"
related_error_codes: ["ERR-3340", "ERR-3305"]
---

# Refresh Failure Retries overview

This page explains how refresh failure retries works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When refresh failure retries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for refresh failure retries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, refresh failure retries is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: refresh failure retries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, refresh failure retries inherits group membership from your identity provider on each login.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
