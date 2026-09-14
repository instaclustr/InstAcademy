---
source_id: "DOC-00930"
title: "How rate limits works"
doc_type: "product-docs"
section_path: "REST API & Embedding > Rate Limits > How rate limits works"
product_area: "api"
product_version: "4.9"
acl: "professional"
updated_at: "2026-03-04"
related_error_codes: ["ERR-6601"]
---

# How rate limits works

Rate Limits lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

Performance tip: rate limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When rate limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for rate limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable rate limits, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, rate limits inherits group membership from your identity provider on each login.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
