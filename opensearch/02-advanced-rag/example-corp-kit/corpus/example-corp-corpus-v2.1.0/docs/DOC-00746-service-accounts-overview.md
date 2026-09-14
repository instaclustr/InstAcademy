---
source_id: "DOC-00746"
title: "Service Accounts overview"
doc_type: "product-docs"
section_path: "REST API & Embedding > Service Accounts > Service Accounts overview"
product_area: "api"
product_version: "5.0"
acl: "public"
updated_at: "2026-05-31"
related_error_codes: ["ERR-6640", "ERR-6601"]
---

# Service Accounts overview

This page explains how service accounts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable service accounts, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for service accounts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: service accounts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, service accounts inherits group membership from your identity provider on each login.

When service accounts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
