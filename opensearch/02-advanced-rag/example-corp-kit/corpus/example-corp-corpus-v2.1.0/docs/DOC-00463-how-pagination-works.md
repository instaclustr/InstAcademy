---
source_id: "DOC-00463"
title: "How pagination works"
doc_type: "product-docs"
section_path: "REST API & Embedding > Pagination > How pagination works"
product_area: "api"
product_version: "4.8"
acl: "public"
updated_at: "2024-11-16"
related_error_codes: ["ERR-6640"]
---

# How pagination works

Pagination is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, pagination is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable pagination, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

When pagination is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for pagination are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: pagination performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
