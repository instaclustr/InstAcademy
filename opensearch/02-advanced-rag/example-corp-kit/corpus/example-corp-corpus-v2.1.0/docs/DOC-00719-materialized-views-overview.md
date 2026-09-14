---
source_id: "DOC-00719"
title: "Materialized Views overview"
doc_type: "product-docs"
section_path: "Datasets > Materialized Views > Materialized Views overview"
product_area: "datasets"
product_version: "5.1"
acl: "public"
updated_at: "2024-12-11"
related_error_codes: ["ERR-3305"]
---

# Materialized Views overview

Materialized Views is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, materialized views is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for materialized views are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, materialized views inherits group membership from your identity provider on each login.

To enable materialized views, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

When materialized views is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-3305: Dataset refresh deadlock

Cause: Concurrent incremental refresh and full refresh acquired locks in opposite order.

Resolution: Stagger refresh schedules or disable overlapping refresh in dataset settings.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
