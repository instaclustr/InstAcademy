---
source_id: "DOC-00556"
title: "How to configure webhook signatures"
doc_type: "product-docs"
section_path: "REST API & Embedding > Webhook Signatures > How to configure webhook signatures"
product_area: "api"
product_version: "5.1"
acl: "public"
updated_at: "2025-10-15"
related_error_codes: ["ERR-6640"]
---

# How to configure webhook signatures

This page explains how webhook signatures works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When webhook signatures is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, webhook signatures is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable webhook signatures, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for webhook signatures are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, webhook signatures inherits group membership from your identity provider on each login.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| retry_count | integer | 2 | Automatic retries before surfacing an error |
| enabled | boolean | true | Turns the feature on for the workspace |
| notify_on_failure | boolean | true | Sends an email to workspace admins on failure |
| max_concurrency | integer | 8 | Upper bound on parallel executions |

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
