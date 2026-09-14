---
source_id: "DOC-00408"
title: "Troubleshooting saved queries"
doc_type: "product-docs"
section_path: "SQL Workbench > Saved Queries > Troubleshooting saved queries"
product_area: "sql-workbench"
product_version: "4.9"
acl: "public"
updated_at: "2026-03-29"
related_error_codes: ["ERR-5501"]
---

# Troubleshooting saved queries

Saved Queries is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, saved queries is limited to 25 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, saved queries inherits group membership from your identity provider on each login.

To enable saved queries, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for saved queries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When saved queries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
