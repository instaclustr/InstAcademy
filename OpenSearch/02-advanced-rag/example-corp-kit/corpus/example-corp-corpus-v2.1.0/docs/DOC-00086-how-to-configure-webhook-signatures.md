---
source_id: "DOC-00086"
title: "How to configure webhook signatures"
doc_type: "product-docs"
section_path: "REST API & Embedding > Webhook Signatures > How to configure webhook signatures"
product_area: "api"
product_version: "4.9"
acl: "public"
updated_at: "2024-01-26"
related_error_codes: ["ERR-6640"]
---

# How to configure webhook signatures

This page explains how webhook signatures works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, webhook signatures inherits group membership from your identity provider on each login.

When webhook signatures is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, webhook signatures is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

To enable webhook signatures, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: webhook signatures performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| max_concurrency | integer | 8 | Upper bound on parallel executions |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| enabled | boolean | true | Turns the feature on for the workspace |

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
