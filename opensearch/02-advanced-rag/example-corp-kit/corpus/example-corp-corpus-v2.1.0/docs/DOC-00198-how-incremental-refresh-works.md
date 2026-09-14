---
source_id: "DOC-00198"
title: "How incremental refresh works"
doc_type: "product-docs"
section_path: "Datasets > Incremental Refresh > How incremental refresh works"
product_area: "datasets"
product_version: "5.1"
acl: "public"
updated_at: "2024-08-30"
related_error_codes: ["ERR-3305"]
---

# How incremental refresh works

This page explains how incremental refresh works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, incremental refresh is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for incremental refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When incremental refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable incremental refresh, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, incremental refresh inherits group membership from your identity provider on each login.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
