---
source_id: "DOC-00510"
title: "Pagination overview"
doc_type: "product-docs"
section_path: "REST API & Embedding > Pagination > Pagination overview"
product_area: "api"
product_version: "4.8"
acl: "public"
updated_at: "2026-01-30"
related_error_codes: ["ERR-6640"]
---

# Pagination overview

Pagination lets your team automate repetitive analysis without leaving Example Corp BI Platform.

## Configuration

By default, pagination is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When pagination is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: pagination performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable pagination, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for pagination are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
