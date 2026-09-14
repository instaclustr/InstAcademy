---
source_id: "DOC-00159"
title: "Troubleshooting SSH tunneling"
doc_type: "product-docs"
section_path: "Data Connectors > Ssh Tunneling > Troubleshooting SSH tunneling"
product_area: "connectors"
product_version: "4.8"
acl: "public"
updated_at: "2025-12-20"
related_error_codes: ["ERR-2209"]
---

# Troubleshooting SSH tunneling

Ssh Tunneling lets your team keep dashboards responsive at scale without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, SSH tunneling inherits group membership from your identity provider on each login.

Performance tip: SSH tunneling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When SSH tunneling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable SSH tunneling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for SSH tunneling are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
