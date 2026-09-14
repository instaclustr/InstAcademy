---
source_id: "DOC-00743"
title: "Signed Embed Urls overview"
doc_type: "product-docs"
section_path: "REST API & Embedding > Signed Embed Urls > Signed Embed Urls overview"
product_area: "api"
product_version: "5.1"
acl: "public"
updated_at: "2026-04-10"
related_error_codes: ["ERR-6640"]
---

# Signed Embed Urls overview

Signed Embed Urls is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

Performance tip: signed embed URLs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable signed embed URLs, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for signed embed URLs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, signed embed URLs inherits group membership from your identity provider on each login.

By default, signed embed URLs is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
