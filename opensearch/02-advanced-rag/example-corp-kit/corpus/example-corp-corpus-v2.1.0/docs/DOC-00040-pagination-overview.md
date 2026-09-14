---
source_id: "DOC-00040"
title: "Pagination overview"
doc_type: "product-docs"
section_path: "REST API & Embedding > Pagination > Pagination overview"
product_area: "api"
product_version: "5.1"
acl: "professional"
updated_at: "2025-03-26"
related_error_codes: ["ERR-6601"]
---

# Pagination overview

This page explains how pagination works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable pagination, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

By default, pagination is limited to 10 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When pagination is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: pagination performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for pagination are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-6601: API rate limit exceeded

Cause: More than 600 requests per minute per service account.

Resolution: Batch requests, add exponential backoff, or request a limit increase.
