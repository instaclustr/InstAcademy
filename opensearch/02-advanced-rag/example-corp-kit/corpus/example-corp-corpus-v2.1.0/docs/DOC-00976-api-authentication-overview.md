---
source_id: "DOC-00976"
title: "Api Authentication overview"
doc_type: "product-docs"
section_path: "REST API & Embedding > Api Authentication > Api Authentication overview"
product_area: "api"
product_version: "5.1"
acl: "enterprise"
updated_at: "2025-08-22"
related_error_codes: ["ERR-6601"]
---

# Api Authentication overview

Api Authentication is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, API authentication is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for API authentication are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: API authentication performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, API authentication inherits group membership from your identity provider on each login.

To enable API authentication, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
