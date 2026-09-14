---
source_id: "DOC-00908"
title: "How refresh failure retries works"
doc_type: "product-docs"
section_path: "Datasets > Refresh Failure Retries > How refresh failure retries works"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2025-11-12"
related_error_codes: ["ERR-3340", "ERR-3305"]
---

# How refresh failure retries works

This page explains how refresh failure retries works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable refresh failure retries, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

By default, refresh failure retries is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, refresh failure retries inherits group membership from your identity provider on each login.

Performance tip: refresh failure retries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for refresh failure retries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
