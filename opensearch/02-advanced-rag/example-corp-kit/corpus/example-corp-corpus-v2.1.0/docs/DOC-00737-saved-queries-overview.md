---
source_id: "DOC-00737"
title: "Saved Queries overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Saved Queries > Saved Queries overview"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2024-07-04"
related_error_codes: ["ERR-5501"]
---

# Saved Queries overview

This page explains how saved queries works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable saved queries, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

When saved queries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, saved queries is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Performance tip: saved queries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, saved queries inherits group membership from your identity provider on each login.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
