---
source_id: "DOC-00041"
title: "Service Accounts overview"
doc_type: "product-docs"
section_path: "REST API & Embedding > Service Accounts > Service Accounts overview"
product_area: "api"
product_version: "5.0"
acl: "public"
updated_at: "2024-03-06"
related_error_codes: ["ERR-6601"]
---

# Service Accounts overview

Service Accounts lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

By default, service accounts is limited to 50 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When service accounts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for service accounts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, service accounts inherits group membership from your identity provider on each login.

To enable service accounts, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
