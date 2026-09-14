---
source_id: "DOC-00226"
title: "How signed embed URLs works"
doc_type: "product-docs"
section_path: "REST API & Embedding > Signed Embed Urls > How signed embed URLs works"
product_area: "api"
product_version: "5.1"
acl: "enterprise"
updated_at: "2025-01-10"
related_error_codes: ["ERR-6640"]
---

# How signed embed URLs works

Signed Embed Urls is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

When signed embed URLs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, signed embed URLs inherits group membership from your identity provider on each login.

Performance tip: signed embed URLs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for signed embed URLs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable signed embed URLs, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
