---
source_id: "DOC-00220"
title: "How saved queries works"
doc_type: "product-docs"
section_path: "SQL Workbench > Saved Queries > How saved queries works"
product_area: "sql-workbench"
product_version: "4.8"
acl: "public"
updated_at: "2026-01-01"
related_error_codes: ["ERR-5501"]
---

# How saved queries works

This page explains how saved queries works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, saved queries inherits group membership from your identity provider on each login.

Audit events for saved queries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When saved queries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, saved queries is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: saved queries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
