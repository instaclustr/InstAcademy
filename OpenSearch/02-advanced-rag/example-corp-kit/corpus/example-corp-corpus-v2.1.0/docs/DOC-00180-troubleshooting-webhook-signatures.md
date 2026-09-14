---
source_id: "DOC-00180"
title: "Troubleshooting webhook signatures"
doc_type: "product-docs"
section_path: "REST API & Embedding > Webhook Signatures > Troubleshooting webhook signatures"
product_area: "api"
product_version: "4.8"
acl: "enterprise"
updated_at: "2026-03-23"
related_error_codes: ["ERR-6601"]
---

# Troubleshooting webhook signatures

Webhook Signatures lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

When webhook signatures is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, webhook signatures inherits group membership from your identity provider on each login.

Audit events for webhook signatures are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: webhook signatures performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

By default, webhook signatures is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
