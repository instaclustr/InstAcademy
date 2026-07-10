---
source_id: "DOC-00882"
title: "Troubleshooting API authentication"
doc_type: "product-docs"
section_path: "REST API & Embedding > Api Authentication > Troubleshooting API authentication"
product_area: "api"
product_version: "4.9"
acl: "public"
updated_at: "2024-06-14"
related_error_codes: ["ERR-6601"]
---

# Troubleshooting API authentication

Api Authentication is available on version 4.9 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Audit events for API authentication are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When API authentication is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, API authentication inherits group membership from your identity provider on each login.

To enable API authentication, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: API authentication performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
