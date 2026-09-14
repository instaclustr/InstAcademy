---
source_id: "DOC-00630"
title: "Troubleshooting IP allowlisting"
doc_type: "product-docs"
section_path: "Data Connectors > Ip Allowlisting > Troubleshooting IP allowlisting"
product_area: "connectors"
product_version: "4.9"
acl: "standard"
updated_at: "2024-04-07"
related_error_codes: ["ERR-2231"]
---

# Troubleshooting IP allowlisting

Ip Allowlisting is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable IP allowlisting, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for IP allowlisting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: IP allowlisting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When IP allowlisting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, IP allowlisting is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
