---
source_id: "GUIDE-004"
title: "Redshift integration guide"
doc_type: "integration-guide"
integration: "Redshift"
category: "warehouse"
section_path: "Integrations > Redshift"
min_version: "4.9"
acl: "public"
updated_at: "2024-11-03"
related_error_codes: ["ERR-2209", "ERR-2288", "ERR-2231"]
---

# Redshift integration guide

Connect Redshift to Example Corp BI Platform to query warehouse data directly from dashboards and the SQL Workbench. Requires platform version 4.9 or later.

## Prerequisites

1. A Redshift account with permission to create credentials
2. Authentication method: IAM
3. Network access from the platform IP ranges to your Redshift endpoint (see the IP allowlisting page)

## Connection settings

| Field | Required | Notes |
| --- | --- | --- |
| Host | Yes | Your Redshift endpoint hostname |
| Port | Yes | Default varies by deployment |
| Credential | Yes | IAM |
| Schema scope | No | Limit discovery to named schemas to avoid ERR-2288 |
| TLS version | No | TLS 1.3 recommended; required by some warehouses |

## Setup steps

1. In the workspace, open Data Connectors and choose Redshift from the catalog.
2. Enter the connection settings above and provide your IAM credential.
3. Run the connection test. A successful test validates network reachability, authentication, and schema access in one pass.
4. Choose the schemas to expose. Scoping schemas speeds up discovery on large catalogs.
5. Save. The connector appears in the dataset builder within one minute.

## Common errors

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

Fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

Fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

## Credential rotation

Rotate Redshift credentials from the connector settings page. Rotation is zero downtime: the platform validates the new credential before retiring the old one. Expired credentials surface as ERR-2231 in the connector health panel.