"""
the support tool shared taxonomy for Example Corp BI Platform.

Every generator imports from this file so error codes, product areas,
versions, and integrations stay consistent across all five data assets.
That consistency is what makes cross-asset retrieval demos work: a ticket
that mentions ERR-2209 will always line up with the known issue record,
the Snowflake integration guide, and the docs page that explain it.
"""

PRODUCT_NAME = "Example Corp BI Platform"
VERSIONS = ["4.8", "4.9", "5.0", "5.1"]
CURRENT_VERSION = "5.1"
PLAN_TIERS = ["standard", "professional", "enterprise"]

PRODUCT_AREAS = {
    "dashboards": {
        "label": "Dashboards",
        "features": [
            "dashboard rendering", "cross-filtering", "drill-down",
            "auto-refresh intervals", "dashboard sharing", "PDF export",
            "mobile layouts", "embedded dashboards",
        ],
    },
    "datasets": {
        "label": "Datasets",
        "features": [
            "dataset refresh scheduling", "incremental refresh",
            "calculated fields", "row-level security", "dataset lineage",
            "materialized views", "refresh failure retries",
        ],
    },
    "connectors": {
        "label": "Data Connectors",
        "features": [
            "connection pooling", "OAuth token refresh", "SSH tunneling",
            "IP allowlisting", "schema discovery", "query pushdown",
            "connector credential rotation",
        ],
    },
    "alerts": {
        "label": "Alerts & Scheduled Reports",
        "features": [
            "threshold alerts", "anomaly alerts", "email delivery",
            "Slack delivery", "webhook delivery", "report bursting",
            "alert throttling",
        ],
    },
    "sql-workbench": {
        "label": "SQL Workbench",
        "features": [
            "query editor", "query history", "saved queries",
            "query timeouts", "result caching", "CSV download limits",
        ],
    },
    "api": {
        "label": "REST API & Embedding",
        "features": [
            "API authentication", "rate limits", "signed embed URLs",
            "webhook signatures", "pagination", "service accounts",
        ],
    },
    "admin": {
        "label": "Administration",
        "features": [
            "SAML SSO", "SCIM provisioning", "audit logs",
            "workspace permissions", "usage analytics", "license seats",
        ],
    },
}

# Error codes are the connective tissue of the whole demo corpus.
# code -> (title, area, cause, workaround, affects_versions, fixed_in)
ERROR_CODES = {
    "ERR-1102": ("Dashboard render timeout", "dashboards",
                 "Widget query exceeded the 60 second render budget",
                 "Reduce widget count or enable result caching on the underlying dataset",
                 ["4.8", "4.9"], "5.0"),
    "ERR-1147": ("Cross-filter loop detected", "dashboards",
                 "Two widgets reference each other as filter sources",
                 "Remove one direction of the cross-filter relationship",
                 ["4.8", "4.9", "5.0", "5.1"], None),
    "ERR-1210": ("PDF export failed: asset too large", "dashboards",
                 "Rendered dashboard exceeds the 50 MB export ceiling",
                 "Export tabs individually or lower image DPI in export settings",
                 ["4.9", "5.0"], "5.1"),
    "ERR-2209": ("Connector handshake failed", "connectors",
                 "TLS negotiation failed because the warehouse requires TLS 1.3",
                 "Enable TLS 1.3 in the connector advanced settings, available in 5.0 and later",
                 ["4.8", "4.9"], "5.0"),
    "ERR-2231": ("OAuth token refresh rejected", "connectors",
                 "Refresh token expired after the identity provider rotated signing keys",
                 "Reauthorize the connection from the connector settings page",
                 ["4.8", "4.9", "5.0", "5.1"], None),
    "ERR-2288": ("Schema discovery timed out", "connectors",
                 "Warehouse information_schema query exceeded 120 seconds on very large catalogs",
                 "Scope the connection to specific schemas instead of the full catalog",
                 ["4.8", "4.9", "5.0"], "5.1"),
    "ERR-3305": ("Dataset refresh deadlock", "datasets",
                 "Concurrent incremental refresh and full refresh acquired locks in opposite order",
                 "Stagger refresh schedules or disable overlapping refresh in dataset settings",
                 ["4.8", "4.9", "5.0"], "5.1"),
    "ERR-3340": ("Row-level security rule not applied", "datasets",
                 "RLS rules referencing calculated fields are evaluated after aggregation",
                 "Rewrite the RLS rule against a raw column, not a calculated field",
                 ["4.8", "4.9", "5.0", "5.1"], None),
    "ERR-4402": ("Alert delivery throttled", "alerts",
                 "More than 100 alert emails to a single recipient within one hour",
                 "Consolidate alerts with report bursting or raise the throttle limit per workspace",
                 ["4.9", "5.0", "5.1"], None),
    "ERR-4415": ("Webhook signature mismatch", "alerts",
                 "Receiving endpoint validated against a rotated webhook secret",
                 "Update the shared secret on the receiver; secrets rotate every 90 days by default",
                 ["5.0", "5.1"], None),
    "ERR-5501": ("Query timeout in SQL Workbench", "sql-workbench",
                 "Interactive queries are capped at 300 seconds on standard tier",
                 "Move long-running queries to a scheduled dataset refresh or upgrade tier limits",
                 ["4.8", "4.9", "5.0", "5.1"], None),
    "ERR-6601": ("API rate limit exceeded", "api",
                 "More than 600 requests per minute per service account",
                 "Batch requests, add exponential backoff, or request a limit increase",
                 ["4.8", "4.9", "5.0", "5.1"], None),
    "ERR-6640": ("Signed embed URL expired", "api",
                 "Embed URLs are valid for 10 minutes; the host page cached one longer",
                 "Generate embed URLs server side per page load, never cache them",
                 ["4.9", "5.0", "5.1"], None),
    "ERR-7719": ("SAML assertion rejected", "admin",
                 "Clock skew between the identity provider and the platform exceeded 5 minutes",
                 "Sync IdP server clocks with NTP; skew tolerance is configurable in 5.1",
                 ["4.8", "4.9", "5.0"], "5.1"),
    "ERR-7733": ("SCIM provisioning conflict", "admin",
                 "A SCIM push tried to create a user whose email already exists as a local account",
                 "Convert the local account to SSO before enabling SCIM for that domain",
                 ["4.9", "5.0", "5.1"], None),
}

INTEGRATIONS = [
    # (name, category, auth_method)
    ("Salesforce", "crm", "OAuth 2.0"),
    ("Snowflake", "warehouse", "key pair"),
    ("BigQuery", "warehouse", "service account JSON"),
    ("Redshift", "warehouse", "IAM"),
    ("Databricks", "warehouse", "personal access token"),
    ("PostgreSQL", "database", "username and password"),
    ("MySQL", "database", "username and password"),
    ("SQL Server", "database", "username and password"),
    ("Oracle", "database", "wallet"),
    ("MongoDB", "database", "connection string"),
    ("Amazon S3", "storage", "IAM"),
    ("Google Cloud Storage", "storage", "service account JSON"),
    ("Azure Blob Storage", "storage", "SAS token"),
    ("Apache Kafka", "streaming", "SASL/SCRAM"),
    ("Apache Cassandra", "database", "username and password"),
    ("OpenSearch", "search", "basic auth over TLS"),
    ("ClickHouse", "warehouse", "username and password"),
    ("HubSpot", "crm", "private app token"),
    ("Zendesk", "support", "API token"),
    ("Jira", "project", "API token"),
    ("ServiceNow", "itsm", "OAuth 2.0"),
    ("Stripe", "billing", "restricted API key"),
    ("NetSuite", "erp", "token-based auth"),
    ("SAP HANA", "erp", "username and password"),
    ("Workday", "hr", "ISU credentials"),
    ("Marketo", "marketing", "OAuth 2.0"),
    ("Google Analytics", "marketing", "OAuth 2.0"),
    ("Google Sheets", "files", "OAuth 2.0"),
    ("Microsoft Excel Online", "files", "OAuth 2.0"),
    ("SharePoint", "files", "OAuth 2.0"),
    ("Dropbox", "files", "OAuth 2.0"),
    ("Box", "files", "OAuth 2.0"),
    ("Shopify", "commerce", "admin API token"),
    ("Amplitude", "analytics", "API key"),
    ("Mixpanel", "analytics", "service account"),
    ("Segment", "analytics", "write key"),
    ("Airtable", "database", "personal access token"),
    ("DynamoDB", "database", "IAM"),
    ("Elasticsearch", "search", "API key"),
    ("Teradata", "warehouse", "username and password"),
    ("Vertica", "warehouse", "username and password"),
    ("Presto", "query", "username and password"),
    ("Trino", "query", "username and password"),
    ("Athena", "query", "IAM"),
    ("Synapse", "warehouse", "service principal"),
    ("Fabric", "warehouse", "service principal"),
    ("Looker Connect", "bi", "API3 credentials"),
    ("dbt Cloud", "transform", "service token"),
    ("Fivetran", "elt", "API key"),
    ("Airbyte", "elt", "API key"),
]

FIRST_NAMES = ["Priya", "Marcus", "Elena", "Tomás", "Aisha", "Derek", "Ingrid",
               "Kenji", "Fatima", "Lucas", "Nadia", "Owen", "Sofia", "Ravi",
               "Hannah", "Diego", "Mei", "Jonas", "Amara", "Colin"]
COMPANY_STEMS = ["Northwind", "Apex", "Bluepeak", "Cedar", "Quantum", "Harbor",
                 "Ironwood", "Vertex", "Solstice", "Granite", "Meridian",
                 "Falcon", "Copper", "Zenith", "Alpine", "Cascade"]
COMPANY_SUFFIXES = ["Logistics", "Financial", "Health", "Retail", "Manufacturing",
                    "Insurance", "Media", "Energy", "Labs", "Systems"]


def tenant_id(rng):
    return f"{rng.choice(COMPANY_STEMS).lower()}-{rng.choice(COMPANY_SUFFIXES).lower()}"
