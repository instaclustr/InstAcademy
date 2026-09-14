---
source_id: "DOC-00741"
title: "Api Authentication overview"
doc_type: "product-docs"
section_path: "REST API & Embedding > Api Authentication > Api Authentication overview"
product_area: "api"
product_version: "4.9"
acl: "public"
updated_at: "2025-03-27"
related_error_codes: ["ERR-6601"]
---

# Api Authentication overview

This page explains how API authentication works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable API authentication, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

By default, API authentication is limited to 10 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When API authentication is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for API authentication are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: API authentication performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
