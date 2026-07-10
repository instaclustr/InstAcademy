---
source_id: "DOC-00205"
title: "How OAuth token refresh works"
doc_type: "product-docs"
section_path: "Data Connectors > Oauth Token Refresh > How OAuth token refresh works"
product_area: "connectors"
product_version: "5.1"
acl: "public"
updated_at: "2025-06-01"
related_error_codes: ["ERR-2288"]
---

# How OAuth token refresh works

Oauth Token Refresh lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

By default, OAuth token refresh is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for OAuth token refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: OAuth token refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable OAuth token refresh, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

When OAuth token refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
