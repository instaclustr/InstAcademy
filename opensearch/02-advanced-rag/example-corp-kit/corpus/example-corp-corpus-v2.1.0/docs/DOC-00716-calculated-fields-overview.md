---
source_id: "DOC-00716"
title: "Calculated Fields overview"
doc_type: "product-docs"
section_path: "Datasets > Calculated Fields > Calculated Fields overview"
product_area: "datasets"
product_version: "5.0"
acl: "public"
updated_at: "2025-07-09"
related_error_codes: ["ERR-3305"]
---

# Calculated Fields overview

This page explains how calculated fields works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When calculated fields is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: calculated fields performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, calculated fields is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable calculated fields, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, calculated fields inherits group membership from your identity provider on each login.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
