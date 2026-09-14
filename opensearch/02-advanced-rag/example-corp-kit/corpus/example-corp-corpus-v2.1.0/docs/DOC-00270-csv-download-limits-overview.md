---
source_id: "DOC-00270"
title: "Csv Download Limits overview"
doc_type: "product-docs"
section_path: "SQL Workbench > Csv Download Limits > Csv Download Limits overview"
product_area: "sql-workbench"
product_version: "5.0"
acl: "public"
updated_at: "2026-02-04"
related_error_codes: ["ERR-5501"]
---

# Csv Download Limits overview

Csv Download Limits is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, CSV download limits is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, CSV download limits inherits group membership from your identity provider on each login.

To enable CSV download limits, open the workspace settings panel and select the SQL Workbench tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for CSV download limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When CSV download limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-5501: Query timeout in SQL Workbench

Cause: Interactive queries are capped at 300 seconds on standard tier.

Resolution: Move long-running queries to a scheduled dataset refresh or upgrade tier limits.
