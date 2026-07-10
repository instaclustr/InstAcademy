---
source_id: "DOC-00914"
title: "How query pushdown works"
doc_type: "product-docs"
section_path: "Data Connectors > Query Pushdown > How query pushdown works"
product_area: "connectors"
product_version: "4.9"
acl: "enterprise"
updated_at: "2025-06-24"
related_error_codes: ["ERR-2231", "ERR-2209"]
---

# How query pushdown works

This page explains how query pushdown works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

By default, query pushdown is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: query pushdown performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for query pushdown are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, query pushdown inherits group membership from your identity provider on each login.

When query pushdown is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
