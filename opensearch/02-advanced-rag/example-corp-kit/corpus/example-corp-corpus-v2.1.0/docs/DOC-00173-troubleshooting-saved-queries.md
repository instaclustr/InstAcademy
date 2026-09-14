---
source_id: "DOC-00173"
title: "Troubleshooting saved queries"
doc_type: "product-docs"
section_path: "SQL Workbench > Saved Queries > Troubleshooting saved queries"
product_area: "sql-workbench"
product_version: "5.1"
acl: "public"
updated_at: "2025-11-30"
related_error_codes: ["ERR-5501"]
---

# Troubleshooting saved queries

This page explains how saved queries works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable saved queries, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, saved queries inherits group membership from your identity provider on each login.

Audit events for saved queries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: saved queries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, saved queries is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
