---
source_id: "GUIDE-032"
title: "Box integration guide"
doc_type: "integration-guide"
integration: "Box"
category: "files"
section_path: "Integrations > Box"
min_version: "4.8"
acl: "public"
updated_at: "2024-09-26"
related_error_codes: ["ERR-2288", "ERR-2231", "ERR-2231"]
---

# Box integration guide

Connect Box to Example Corp BI Platform to query files data directly from dashboards and the SQL Workbench. Requires platform version 4.8 or later.

## Prerequisites

1. A Box account with permission to create credentials
2. Authentication method: OAuth 2.0
3. Network access from the platform IP ranges to your Box endpoint (see the IP allowlisting page)

## Connection settings

| Field | Required | Notes |
| --- | --- | --- |
| Host | Yes | Your Box endpoint hostname |
| Port | Yes | Default varies by deployment |
| Credential | Yes | OAuth 2.0 |
| Schema scope | No | Limit discovery to named schemas to avoid ERR-2288 |
| TLS version | No | TLS 1.3 recommended; required by some warehouses |

## Setup steps

1. In the workspace, open Data Connectors and choose Box from the catalog.
2. Enter the connection settings above and provide your OAuth 2.0 credential.
3. Run the connection test. A successful test validates network reachability, authentication, and schema access in one pass.
4. Choose the schemas to expose. Scoping schemas speeds up discovery on large catalogs.
5. Save. The connector appears in the dataset builder within one minute.

## Common errors

### ERR-2288: Schema discovery timed out

Cause: Warehouse information_schema query exceeded 120 seconds on very large catalogs.

Resolution: Scope the connection to specific schemas instead of the full catalog.

Fixed in version 5.1. Affected versions: 4.8, 4.9, 5.0.

### ERR-2231: OAuth token refresh rejected

Cause: Refresh token expired after the identity provider rotated signing keys.

Resolution: Reauthorize the connection from the connector settings page.

## Credential rotation

Rotate Box credentials from the connector settings page. Rotation is zero downtime: the platform validates the new credential before retiring the old one. Expired credentials surface as ERR-2231 in the connector health panel.