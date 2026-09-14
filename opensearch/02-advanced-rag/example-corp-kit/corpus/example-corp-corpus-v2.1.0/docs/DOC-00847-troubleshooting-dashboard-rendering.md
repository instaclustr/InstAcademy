---
source_id: "DOC-00847"
title: "Troubleshooting dashboard rendering"
doc_type: "product-docs"
section_path: "Dashboards > Dashboard Rendering > Troubleshooting dashboard rendering"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2024-03-26"
related_error_codes: ["ERR-1147"]
---

# Troubleshooting dashboard rendering

This page explains how dashboard rendering works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for dashboard rendering are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When dashboard rendering is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, dashboard rendering is limited to 100 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable dashboard rendering, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: dashboard rendering performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
