---
source_id: "DOC-00940"
title: "How license seats works"
doc_type: "product-docs"
section_path: "Administration > License Seats > How license seats works"
product_area: "admin"
product_version: "4.9"
acl: "public"
updated_at: "2024-06-09"
related_error_codes: ["ERR-7733"]
---

# How license seats works

This page explains how license seats works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When license seats is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for license seats are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: license seats performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable license seats, open the workspace settings panel and select the Administration tab. Changes apply within one refresh cycle and do not require a restart.

By default, license seats is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-7733: SCIM provisioning conflict

Cause: A SCIM push tried to create a user whose email already exists as a local account.

Resolution: Convert the local account to SSO before enabling SCIM for that domain.
