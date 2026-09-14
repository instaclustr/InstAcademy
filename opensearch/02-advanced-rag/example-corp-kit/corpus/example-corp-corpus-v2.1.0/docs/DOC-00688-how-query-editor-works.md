---
source_id: "DOC-00688"
title: "How query editor works"
doc_type: "product-docs"
section_path: "SQL Workbench > Query Editor > How query editor works"
product_area: "sql-workbench"
product_version: "4.9"
acl: "enterprise"
updated_at: "2025-06-13"
related_error_codes: ["ERR-5501"]
---

# How query editor works

This page explains how query editor works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for query editor are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, query editor inherits group membership from your identity provider on each login.

By default, query editor is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: query editor performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When query editor is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
