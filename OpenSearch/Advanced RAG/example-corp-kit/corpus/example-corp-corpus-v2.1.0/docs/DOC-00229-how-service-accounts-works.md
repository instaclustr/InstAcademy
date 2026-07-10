---
source_id: "DOC-00229"
title: "How service accounts works"
doc_type: "product-docs"
section_path: "REST API & Embedding > Service Accounts > How service accounts works"
product_area: "api"
product_version: "5.1"
acl: "professional"
updated_at: "2025-09-25"
related_error_codes: ["ERR-6601"]
---

# How service accounts works

This page explains how service accounts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When service accounts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable service accounts, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

By default, service accounts is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for service accounts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, service accounts inherits group membership from your identity provider on each login.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
