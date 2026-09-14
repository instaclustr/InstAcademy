---
source_id: "DOC-00182"
title: "Troubleshooting service accounts"
doc_type: "product-docs"
section_path: "REST API & Embedding > Service Accounts > Troubleshooting service accounts"
product_area: "api"
product_version: "5.1"
acl: "public"
updated_at: "2025-01-26"
related_error_codes: ["ERR-6601"]
---

# Troubleshooting service accounts

Service Accounts is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, service accounts is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, service accounts inherits group membership from your identity provider on each login.

To enable service accounts, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for service accounts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When service accounts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
