---
source_id: "DOC-00133"
title: "Webhook Signatures settings reference"
doc_type: "product-docs"
section_path: "REST API & Embedding > Webhook Signatures > Webhook Signatures settings reference"
product_area: "api"
product_version: "5.1"
acl: "public"
updated_at: "2024-06-13"
related_error_codes: ["ERR-6640"]
---

# Webhook Signatures settings reference

Webhook Signatures lets your team reduce time to insight without leaving Example Corp BI Platform.

## Configuration

To enable webhook signatures, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: webhook signatures performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, webhook signatures inherits group membership from your identity provider on each login.

By default, webhook signatures is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for webhook signatures are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| timeout_seconds | integer | 300 | Hard stop for a single execution |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| enabled | boolean | true | Turns the feature on for the workspace |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
