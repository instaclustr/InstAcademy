---
source_id: "DOC-00039"
title: "Webhook Signatures overview"
doc_type: "product-docs"
section_path: "REST API & Embedding > Webhook Signatures > Webhook Signatures overview"
product_area: "api"
product_version: "5.1"
acl: "public"
updated_at: "2025-04-03"
related_error_codes: ["ERR-6601"]
---

# Webhook Signatures overview

Webhook Signatures is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When webhook signatures is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for webhook signatures are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable webhook signatures, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, webhook signatures inherits group membership from your identity provider on each login.

Performance tip: webhook signatures performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
