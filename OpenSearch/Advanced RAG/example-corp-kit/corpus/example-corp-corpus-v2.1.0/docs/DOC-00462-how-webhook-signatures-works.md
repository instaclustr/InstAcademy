---
source_id: "DOC-00462"
title: "How webhook signatures works"
doc_type: "product-docs"
section_path: "REST API & Embedding > Webhook Signatures > How webhook signatures works"
product_area: "api"
product_version: "4.9"
acl: "enterprise"
updated_at: "2024-08-16"
related_error_codes: ["ERR-6640", "ERR-6601"]
---

# How webhook signatures works

This page explains how webhook signatures works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When webhook signatures is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, webhook signatures inherits group membership from your identity provider on each login.

To enable webhook signatures, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

By default, webhook signatures is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for webhook signatures are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
