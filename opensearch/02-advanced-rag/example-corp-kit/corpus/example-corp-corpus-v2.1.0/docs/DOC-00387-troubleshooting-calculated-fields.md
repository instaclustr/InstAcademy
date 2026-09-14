---
source_id: "DOC-00387"
title: "Troubleshooting calculated fields"
doc_type: "product-docs"
section_path: "Datasets > Calculated Fields > Troubleshooting calculated fields"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2024-02-19"
related_error_codes: ["ERR-3340", "ERR-3305"]
---

# Troubleshooting calculated fields

This page explains how calculated fields works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable calculated fields, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

By default, calculated fields is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, calculated fields inherits group membership from your identity provider on each login.

Audit events for calculated fields are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When calculated fields is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
