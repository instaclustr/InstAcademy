---
source_id: "DOC-00717"
title: "Row-Level Security overview"
doc_type: "product-docs"
section_path: "Datasets > Row-Level Security > Row-Level Security overview"
product_area: "datasets"
product_version: "4.9"
acl: "professional"
updated_at: "2026-03-28"
related_error_codes: ["ERR-3305"]
---

# Row-Level Security overview

Row-Level Security is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable row-level security, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

When row-level security is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, row-level security inherits group membership from your identity provider on each login.

Audit events for row-level security are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, row-level security is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
