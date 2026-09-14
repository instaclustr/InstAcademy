---
source_id: "DOC-00863"
title: "Troubleshooting OAuth token refresh"
doc_type: "product-docs"
section_path: "Data Connectors > Oauth Token Refresh > Troubleshooting OAuth token refresh"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2026-03-05"
related_error_codes: ["ERR-2288"]
---

# Troubleshooting OAuth token refresh

Oauth Token Refresh lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

If your organization uses SAML SSO, OAuth token refresh inherits group membership from your identity provider on each login.

Audit events for OAuth token refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: OAuth token refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When OAuth token refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, OAuth token refresh is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
