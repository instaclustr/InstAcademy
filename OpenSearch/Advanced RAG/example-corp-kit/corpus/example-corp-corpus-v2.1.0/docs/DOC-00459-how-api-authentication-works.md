---
source_id: "DOC-00459"
title: "How API authentication works"
doc_type: "product-docs"
section_path: "REST API & Embedding > Api Authentication > How API authentication works"
product_area: "api"
product_version: "5.0"
acl: "enterprise"
updated_at: "2026-02-04"
related_error_codes: ["ERR-6601"]
---

# How API authentication works

Api Authentication is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable API authentication, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, API authentication inherits group membership from your identity provider on each login.

When API authentication is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: API authentication performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for API authentication are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
