---
source_id: "DOC-00257"
title: "Connector Credential Rotation overview"
doc_type: "product-docs"
section_path: "Data Connectors > Connector Credential Rotation > Connector Credential Rotation overview"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2024-06-08"
related_error_codes: ["ERR-2231"]
---

# Connector Credential Rotation overview

Connector Credential Rotation is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for connector credential rotation are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable connector credential rotation, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

By default, connector credential rotation is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: connector credential rotation performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When connector credential rotation is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
