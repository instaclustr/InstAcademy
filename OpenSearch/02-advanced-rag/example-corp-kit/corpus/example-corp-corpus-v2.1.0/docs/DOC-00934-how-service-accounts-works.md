---
source_id: "DOC-00934"
title: "How service accounts works"
doc_type: "product-docs"
section_path: "REST API & Embedding > Service Accounts > How service accounts works"
product_area: "api"
product_version: "4.9"
acl: "public"
updated_at: "2025-08-06"
related_error_codes: ["ERR-6640"]
---

# How service accounts works

Service Accounts lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

When service accounts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for service accounts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: service accounts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, service accounts inherits group membership from your identity provider on each login.

To enable service accounts, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
