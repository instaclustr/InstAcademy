---
source_id: "DOC-00453"
title: "How query editor works"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Editor > How query editor works"
product_area: "sql-workbench"
product_version: "5.1"
acl: "standard"
updated_at: "2024-05-23"
related_error_codes: ["ERR-5501"]
---

# How query editor works

This page explains how query editor works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: query editor performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, query editor inherits group membership from your identity provider on each login.

When query editor is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable query editor, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for query editor are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
