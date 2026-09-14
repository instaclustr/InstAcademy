---
source_id: "DOC-00163"
title: "Troubleshooting connector credential rotation"
doc_type: "product-docs"
section_path: "Data Connectors > Connector Credential Rotation > Troubleshooting connector credential rotation"
product_area: "connectors"
product_version: "4.8"
acl: "enterprise"
updated_at: "2025-01-23"
related_error_codes: ["ERR-2288"]
---

# Troubleshooting connector credential rotation

This page explains how connector credential rotation works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, connector credential rotation inherits group membership from your identity provider on each login.

Audit events for connector credential rotation are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When connector credential rotation is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, connector credential rotation is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable connector credential rotation, open the workspace settings panel and select the Data Connectors tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

This issue is fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.
