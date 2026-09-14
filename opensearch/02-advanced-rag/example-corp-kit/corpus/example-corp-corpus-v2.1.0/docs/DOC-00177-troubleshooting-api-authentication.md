---
source_id: "DOC-00177"
title: "Troubleshooting API authentication"
doc_type: "product-docs"
section_path: "REST API & Embedding > Api Authentication > Troubleshooting API authentication"
product_area: "api"
product_version: "4.8"
acl: "enterprise"
updated_at: "2025-04-13"
related_error_codes: ["ERR-6640"]
---

# Troubleshooting API authentication

Api Authentication is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: API authentication performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When API authentication is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, API authentication inherits group membership from your identity provider on each login.

To enable API authentication, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for API authentication are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
