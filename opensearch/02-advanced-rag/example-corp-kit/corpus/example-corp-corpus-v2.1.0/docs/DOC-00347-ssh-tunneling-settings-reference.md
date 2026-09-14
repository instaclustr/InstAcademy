---
source_id: "DOC-00347"
title: "Ssh Tunneling settings reference"
doc_type: "product-docs"
section_path: "Data Connectors > Ssh Tunneling > Ssh Tunneling settings reference"
product_area: "connectors"
product_version: "4.9"
acl: "standard"
updated_at: "2025-02-08"
related_error_codes: ["ERR-2288"]
---

# Ssh Tunneling settings reference

Ssh Tunneling is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for SSH tunneling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable SSH tunneling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

When SSH tunneling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, SSH tunneling is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: SSH tunneling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
