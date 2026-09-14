---
source_id: "DOC-00878"
title: "Troubleshooting saved queries"
doc_type: "product-docs"
section_path: "SQL Workbench > Saved Queries > Troubleshooting saved queries"
product_area: "sql-workbench"
product_version: "5.0"
acl: "professional"
updated_at: "2026-02-16"
related_error_codes: ["ERR-5501"]
---

# Troubleshooting saved queries

This page explains how saved queries works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: saved queries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable saved queries, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, saved queries inherits group membership from your identity provider on each login.

When saved queries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for saved queries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
