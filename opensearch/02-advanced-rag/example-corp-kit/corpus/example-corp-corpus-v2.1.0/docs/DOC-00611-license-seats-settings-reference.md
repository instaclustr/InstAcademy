---
source_id: "DOC-00611"
title: "License Seats settings reference"
doc_type: "product-docs"
section_path: "Administration > License Seats > License Seats settings reference"
product_area: "admin"
product_version: "5.1"
acl: "standard"
updated_at: "2025-05-01"
related_error_codes: ["ERR-7719"]
---

# License Seats settings reference

This page explains how license seats works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for license seats are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable license seats, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

When license seats is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, license seats is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: license seats performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-7719: SAML assertion rejected

Cause: Clock skew between the identity provider and the platform exceeded 5 minutes.

Resolution: Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
