---
source_id: "DOC-00457"
title: "How result caching works"
doc_type: "product-docs"
section_path: "SQL Workbench > Result Caching > How result caching works"
product_area: "sql-workbench"
product_version: "4.9"
acl: "public"
updated_at: "2025-02-25"
related_error_codes: ["ERR-5501"]
---

# How result caching works

This page explains how result caching works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: result caching performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, result caching is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for result caching are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable result caching, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, result caching inherits group membership from your identity provider on each login.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
