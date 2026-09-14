---
source_id: "DOC-00394"
title: "Troubleshooting SSH tunneling"
doc_type: "product-docs"
section_path: "Data Connectors > Ssh Tunneling > Troubleshooting SSH tunneling"
product_area: "connectors"
product_version: "4.9"
acl: "enterprise"
updated_at: "2025-09-05"
related_error_codes: ["ERR-2231"]
---

# Troubleshooting SSH tunneling

Ssh Tunneling is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: SSH tunneling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable SSH tunneling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

When SSH tunneling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, SSH tunneling inherits group membership from your identity provider on each login.

Audit events for SSH tunneling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.
