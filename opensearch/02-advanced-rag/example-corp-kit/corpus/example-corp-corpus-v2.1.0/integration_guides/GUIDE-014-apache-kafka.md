---
source_id: "GUIDE-014"
title: "Apache Kafka integration guide"
doc_type: "integration-guide"
integration: "Apache Kafka"
category: "streaming"
section_path: "Integrations > Apache Kafka"
min_version: "5.0"
acl: "public"
updated_at: "2024-09-25"
related_error_codes: ["ERR-2231", "ERR-2209", "ERR-2231"]
---

# Apache Kafka integration guide

Connect Apache Kafka to Example Corp BI Platform to query streaming data directly from dashboards and the SQL Workbench. Requires platform version 5.0 or later.

## Prerequisites

1. A Apache Kafka account with permission to create credentials
2. Authentication method: SASL/SCRAM
3. Network access from the platform IP ranges to your Apache Kafka endpoint (see the IP allowlisting page)

## Connection settings

| Field | Required | Notes |
| --- | --- | --- |
| Host | Yes | Your Apache Kafka endpoint hostname |
| Port | Yes | Default varies by deployment |
| Credential | Yes | SASL/SCRAM |
| Schema scope | No | Limit discovery to named schemas to avoid ERR-2288 |
| TLS version | No | TLS 1.3 recommended; required by some warehouses |

## Setup steps

1. In the workspace, open Data Connectors and choose Apache Kafka from the catalog.
2. Enter the connection settings above and provide your SASL/SCRAM credential.
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

Rotate Apache Kafka credentials from the connector settings page. Rotation is zero downtime: the platform validates the new credential before retiring the old one. Expired credentials surface as ERR-2231 in the connector health panel.