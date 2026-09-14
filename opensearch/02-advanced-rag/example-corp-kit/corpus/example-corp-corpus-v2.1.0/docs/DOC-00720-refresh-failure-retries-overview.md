---
source_id: "DOC-00720"
title: "Refresh Failure Retries overview"
doc_type: "product-docs"
section_path: "Datasets > Refresh Failure Retries > Refresh Failure Retries overview"
product_area: "datasets"
product_version: "5.1"
acl: "public"
updated_at: "2026-01-22"
related_error_codes: ["ERR-3305"]
---

# Refresh Failure Retries overview

Refresh Failure Retries lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

When refresh failure retries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for refresh failure retries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, refresh failure retries inherits group membership from your identity provider on each login.

By default, refresh failure retries is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable refresh failure retries, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
