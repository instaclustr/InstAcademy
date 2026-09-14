---
source_id: "DOC-00139"
title: "Workspace Permissions settings reference"
doc_type: "product-docs"
section_path: "Administration > Workspace Permissions > Workspace Permissions settings reference"
product_area: "admin"
product_version: "4.8"
acl: "public"
updated_at: "2026-01-13"
related_error_codes: ["ERR-7733"]
---

# Workspace Permissions settings reference

This page explains how workspace permissions works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: workspace permissions performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable workspace permissions, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

When workspace permissions is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for workspace permissions are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, workspace permissions is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
