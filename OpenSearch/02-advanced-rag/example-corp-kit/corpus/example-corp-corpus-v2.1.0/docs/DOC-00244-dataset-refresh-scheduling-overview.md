---
source_id: "DOC-00244"
title: "Dataset Refresh Scheduling overview"
doc_type: "product-docs"
section_path: "Datasets > Dataset Refresh Scheduling > Dataset Refresh Scheduling overview"
product_area: "datasets"
product_version: "4.8"
acl: "standard"
updated_at: "2025-08-08"
related_error_codes: ["ERR-3305"]
---

# Dataset Refresh Scheduling overview

Dataset Refresh Scheduling is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When dataset refresh scheduling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for dataset refresh scheduling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, dataset refresh scheduling is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable dataset refresh scheduling, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, dataset refresh scheduling inherits group membership from your identity provider on each login.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
