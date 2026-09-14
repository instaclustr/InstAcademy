---
source_id: "DOC-00365"
title: "Api Authentication settings reference"
doc_type: "product-docs"
section_path: "REST API & Embedding > Api Authentication > Api Authentication settings reference"
product_area: "api"
product_version: "5.1"
acl: "public"
updated_at: "2025-05-30"
related_error_codes: ["ERR-6640"]
---

# Api Authentication settings reference

This page explains how API authentication works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for API authentication are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable API authentication, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: API authentication performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When API authentication is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, API authentication is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| timeout_seconds | integer | 300 | Hard stop for a single execution |

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
