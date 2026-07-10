---
source_id: "DOC-00204"
title: "How connection pooling works"
doc_type: "product-docs"
section_path: "Data Connectors > Connection Pooling > How connection pooling works"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2024-10-17"
related_error_codes: ["ERR-2209"]
---

# How connection pooling works

This page explains how connection pooling works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, connection pooling is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Performance tip: connection pooling performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, connection pooling inherits group membership from your identity provider on each login.

When connection pooling is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable connection pooling, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
