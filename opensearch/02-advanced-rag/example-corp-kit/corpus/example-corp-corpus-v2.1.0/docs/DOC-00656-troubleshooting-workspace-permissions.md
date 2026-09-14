---
source_id: "DOC-00656"
title: "Troubleshooting workspace permissions"
doc_type: "product-docs"
section_path: "Administration > Workspace Permissions > Troubleshooting workspace permissions"
product_area: "admin"
product_version: "5.0"
acl: "public"
updated_at: "2024-07-24"
related_error_codes: ["ERR-7733"]
---

# Troubleshooting workspace permissions

Workspace Permissions lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

By default, workspace permissions is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: workspace permissions performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable workspace permissions, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for workspace permissions are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When workspace permissions is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
