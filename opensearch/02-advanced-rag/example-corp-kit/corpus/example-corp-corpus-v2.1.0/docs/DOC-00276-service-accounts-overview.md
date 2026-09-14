---
source_id: "DOC-00276"
title: "Service Accounts overview"
doc_type: "product-docs"
section_path: "REST API & Embedding > Service Accounts > Service Accounts overview"
product_area: "api"
product_version: "4.9"
acl: "public"
updated_at: "2024-12-16"
related_error_codes: ["ERR-6640"]
---

# Service Accounts overview

This page explains how service accounts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable service accounts, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

When service accounts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, service accounts is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Audit events for service accounts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: service accounts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
