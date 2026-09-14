---
source_id: "DOC-00361"
title: "Saved Queries settings reference"
doc_type: "product-docs"
section_path: "SQL Workbench > Saved Queries > Saved Queries settings reference"
product_area: "sql-workbench"
product_version: "5.1"
acl: "public"
updated_at: "2025-01-14"
related_error_codes: ["ERR-5501"]
---

# Saved Queries settings reference

Saved Queries lets your team standardize reporting without leaving Example Corp BI Platform.

## Configuration

Audit events for saved queries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, saved queries inherits group membership from your identity provider on each login.

By default, saved queries is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: saved queries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When saved queries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
