---
source_id: "DOC-00858"
title: "Troubleshooting row-level security"
doc_type: "product-docs"
section_path: "Datasets > Row-Level Security > Troubleshooting row-level security"
product_area: "datasets"
product_version: "4.8"
acl: "public"
updated_at: "2025-01-19"
related_error_codes: ["ERR-3305"]
---

# Troubleshooting row-level security

Row-Level Security is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: row-level security performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, row-level security inherits group membership from your identity provider on each login.

When row-level security is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for row-level security are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable row-level security, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
