---
source_id: "DOC-00902"
title: "How dataset refresh scheduling works"
doc_type: "product-docs"
section_path: "Datasets > Dataset Refresh Scheduling > How dataset refresh scheduling works"
product_area: "datasets"
product_version: "4.9"
acl: "public"
updated_at: "2026-02-15"
related_error_codes: ["ERR-3305"]
---

# How dataset refresh scheduling works

Dataset Refresh Scheduling is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, dataset refresh scheduling inherits group membership from your identity provider on each login.

By default, dataset refresh scheduling is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable dataset refresh scheduling, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for dataset refresh scheduling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: dataset refresh scheduling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
