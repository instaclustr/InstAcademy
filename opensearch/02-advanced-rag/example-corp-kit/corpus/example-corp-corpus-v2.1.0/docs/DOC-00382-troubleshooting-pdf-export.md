---
source_id: "DOC-00382"
title: "Troubleshooting PDF export"
doc_type: "product-docs"
section_path: "Dashboards > Pdf Export > Troubleshooting PDF export"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2026-06-20"
related_error_codes: ["ERR-1147"]
---

# Troubleshooting PDF export

This page explains how PDF export works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for PDF export are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable PDF export, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

By default, PDF export is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: PDF export performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When PDF export is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
