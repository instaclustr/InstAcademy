---
source_id: "DOC-00949"
title: "Dataset Refresh Scheduling overview"
doc_type: "product-docs"
section_path: "Datasets > Dataset Refresh Scheduling > Dataset Refresh Scheduling overview"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2025-10-03"
related_error_codes: ["ERR-3305", "ERR-3340"]
---

# Dataset Refresh Scheduling overview

This page explains how dataset refresh scheduling works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, dataset refresh scheduling inherits group membership from your identity provider on each login.

Audit events for dataset refresh scheduling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, dataset refresh scheduling is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When dataset refresh scheduling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: dataset refresh scheduling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
