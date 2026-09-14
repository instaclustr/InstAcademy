---
source_id: "DOC-00153"
title: "Troubleshooting row-level security"
doc_type: "product-docs"
section_path: "Datasets > Row-Level Security > Troubleshooting row-level security"
product_area: "datasets"
product_version: "4.8"
acl: "public"
updated_at: "2025-03-03"
related_error_codes: ["ERR-3305", "ERR-3340"]
---

# Troubleshooting row-level security

This page explains how row-level security works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: row-level security performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, row-level security inherits group membership from your identity provider on each login.

When row-level security is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable row-level security, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

By default, row-level security is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
