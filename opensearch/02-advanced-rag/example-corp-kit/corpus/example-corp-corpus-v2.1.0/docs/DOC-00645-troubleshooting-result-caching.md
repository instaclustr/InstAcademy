---
source_id: "DOC-00645"
title: "Troubleshooting result caching"
doc_type: "product-docs"
section_path: "SQL Workbench > Result Caching > Troubleshooting result caching"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2024-08-02"
related_error_codes: ["ERR-5501"]
---

# Troubleshooting result caching

This page explains how result caching works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When result caching is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, result caching inherits group membership from your identity provider on each login.

Audit events for result caching are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable result caching, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: result caching performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
