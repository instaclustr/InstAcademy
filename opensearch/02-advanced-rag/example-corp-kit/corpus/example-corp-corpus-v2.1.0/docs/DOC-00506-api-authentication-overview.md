---
source_id: "DOC-00506"
title: "Api Authentication overview"
doc_type: "product-docs"
section_path: "REST API & Embedding > Api Authentication > Api Authentication overview"
product_area: "api"
product_version: "4.8"
acl: "public"
updated_at: "2025-01-02"
related_error_codes: ["ERR-6601", "ERR-6640"]
---

# Api Authentication overview

This page explains how API authentication works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for API authentication are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: API authentication performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, API authentication inherits group membership from your identity provider on each login.

By default, API authentication is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable API authentication, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
