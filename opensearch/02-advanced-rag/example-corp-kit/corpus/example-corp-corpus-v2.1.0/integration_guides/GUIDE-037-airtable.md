---
source_id: "GUIDE-037"
title: "Airtable integration guide"
doc_type: "integration-guide"
integration: "Airtable"
category: "database"
section_path: "Integrations > Airtable"
min_version: "4.9"
acl: "public"
updated_at: "2026-03-08"
related_error_codes: ["ERR-2231", "ERR-2209", "ERR-2231"]
---

# Airtable integration guide

Connect Airtable to Example Corp BI Platform to query database data directly from dashboards and the SQL Workbench. Requires platform version 4.9 or later.

## Prerequisites

1. A Airtable account with permission to create credentials
2. Authentication method: personal access token
3. Network access from the platform IP ranges to your Airtable endpoint (see the IP allowlisting page)

## Connection settings

| Field | Required | Notes |
| --- | --- | --- |
| Host | Yes | Your Airtable endpoint hostname |
| Port | Yes | Default varies by deployment |
| Credential | Yes | personal access token |
| Schema scope | No | Limit discovery to named schemas to avoid ERR-2288 |
| TLS version | No | TLS 1.3 recommended; required by some warehouses |

## Setup steps

1. In the workspace, open Data Connectors and choose Airtable from the catalog.
2. Enter the connection settings above and provide your personal access token credential.
3. Run the connection test. A successful test validates network reachability, authentication, and schema access in one pass.
4. Choose the schemas to expose. Scoping schemas speeds up discovery on large catalogs.
5. Save. The connector appears in the dataset builder within one minute.

## Common errors

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.

### ERR-2209: Connector handshake failed

Cause: TLS negotiation failed because the warehouse requires TLS 1.3.

Resolution: Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later.

Fixed in version 5.0. Affected versions: 4.8, 4.9.

## Credential rotation

Rotate Airtable credentials from the connector settings page. Rotation is zero downtime: the platform validates the new credential before retiring the old one. Expired credentials surface as ERR-2231 in the connector health panel.