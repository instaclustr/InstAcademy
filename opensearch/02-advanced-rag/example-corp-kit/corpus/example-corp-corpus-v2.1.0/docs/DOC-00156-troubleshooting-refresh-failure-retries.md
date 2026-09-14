---
source_id: "DOC-00156"
title: "Troubleshooting refresh failure retries"
doc_type: "product-docs"
section_path: "Datasets > Refresh Failure Retries > Troubleshooting refresh failure retries"
product_area: "datasets"
product_version: "5.0"
acl: "public"
updated_at: "2024-06-16"
related_error_codes: ["ERR-3305"]
---

# Troubleshooting refresh failure retries

Refresh Failure Retries lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

Audit events for refresh failure retries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: refresh failure retries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When refresh failure retries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, refresh failure retries is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, refresh failure retries inherits group membership from your identity provider on each login.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
