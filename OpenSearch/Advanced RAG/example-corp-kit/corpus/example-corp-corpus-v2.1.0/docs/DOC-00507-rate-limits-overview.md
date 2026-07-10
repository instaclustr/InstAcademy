---
source_id: "DOC-00507"
title: "Rate Limits overview"
doc_type: "product-docs"
section_path: "REST API & Embedding > Rate Limits > Rate Limits overview"
product_area: "api"
product_version: "4.9"
acl: "professional"
updated_at: "2025-01-31"
related_error_codes: ["ERR-6640"]
---

# Rate Limits overview

This page explains how rate limits works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When rate limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, rate limits is limited to 25 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for rate limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: rate limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

To enable rate limits, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
