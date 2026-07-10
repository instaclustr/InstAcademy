---
source_id: "DOC-00883"
title: "Troubleshooting rate limits"
doc_type: "product-docs"
section_path: "REST API & Embedding > Rate Limits > Troubleshooting rate limits"
product_area: "api"
product_version: "5.1"
acl: "standard"
updated_at: "2024-04-24"
related_error_codes: ["ERR-6640"]
---

# Troubleshooting rate limits

This page explains how rate limits works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for rate limits are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable rate limits, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

By default, rate limits is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: rate limits performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When rate limits is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
