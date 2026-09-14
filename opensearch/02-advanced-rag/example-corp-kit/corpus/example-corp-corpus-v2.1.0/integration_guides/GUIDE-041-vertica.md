---
source_id: "GUIDE-041"
title: "Vertica integration guide"
doc_type: "integration-guide"
integration: "Vertica"
category: "warehouse"
section_path: "Integrations > Vertica"
min_version: "4.9"
acl: "public"
updated_at: "2026-01-25"
related_error_codes: ["ERR-2209", "ERR-2288", "ERR-2231"]
---

# Vertica integration guide

Connect Vertica to Example Corp BI Platform to query warehouse data directly from dashboards and the SQL Workbench. Requires platform version 4.9 or later.

## Prerequisites

1. A Vertica account with permission to create credentials
2. Authentication method: username and password
3. Network access from the platform IP ranges to your Vertica endpoint (see the IP allowlisting page)

## Connection settings

| Field | Required | Notes |
| --- | --- | --- |
| Host | Yes | Your Vertica endpoint hostname |
| Port | Yes | Default varies by deployment |
| Credential | Yes | username and password |
| Schema scope | No | Limit discovery to named schemas to avoid ERR-2288 |
| TLS version | No | TLS 1.3 recommended; required by some warehouses |

## Setup steps

1. In the workspace, open Data Connectors and choose Vertica from the catalog.
2. Enter the connection settings above and provide your username and password credential.
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

Rotate Vertica credentials from the connector settings page. Rotation is zero downtime: the platform validates the new credential before retiring the old one. Expired credentials surface as ERR-2231 in the connector health panel.