---
source_id: "DOC-00932"
title: "How webhook signatures works"
doc_type: "product-docs"
section_path: "REST API & Embedding > Webhook Signatures > How webhook signatures works"
product_area: "api"
product_version: "5.1"
acl: "public"
updated_at: "2025-02-07"
related_error_codes: ["ERR-6640"]
---

# How webhook signatures works

This page explains how webhook signatures works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: webhook signatures performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for webhook signatures are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

If your organization uses SAML SSO, webhook signatures inherits group membership from your identity provider on each login.

By default, webhook signatures is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

To enable webhook signatures, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
