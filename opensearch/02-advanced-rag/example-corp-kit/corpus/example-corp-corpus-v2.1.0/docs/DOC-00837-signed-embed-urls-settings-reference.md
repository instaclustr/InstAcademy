---
source_id: "DOC-00837"
title: "Signed Embed Urls settings reference"
doc_type: "product-docs"
section_path: "REST API & Embedding > Signed Embed Urls > Signed Embed Urls settings reference"
product_area: "api"
product_version: "4.9"
acl: "public"
updated_at: "2026-04-28"
related_error_codes: ["ERR-6640"]
---

# Signed Embed Urls settings reference

This page explains how signed embed URLs works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable signed embed URLs, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: signed embed URLs performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for signed embed URLs are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, signed embed URLs is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When signed embed URLs is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
