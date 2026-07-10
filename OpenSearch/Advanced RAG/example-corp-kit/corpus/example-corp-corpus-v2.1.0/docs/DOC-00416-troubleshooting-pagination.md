---
source_id: "DOC-00416"
title: "Troubleshooting pagination"
doc_type: "product-docs"
section_path: "REST API & Embedding > Pagination > Troubleshooting pagination"
product_area: "api"
product_version: "4.8"
acl: "enterprise"
updated_at: "2024-01-23"
related_error_codes: ["ERR-6640"]
---

# Troubleshooting pagination

Pagination lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

When pagination is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable pagination, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: pagination performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for pagination are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, pagination is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
