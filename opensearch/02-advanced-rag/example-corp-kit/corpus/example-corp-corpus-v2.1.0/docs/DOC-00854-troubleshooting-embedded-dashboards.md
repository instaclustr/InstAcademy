---
source_id: "DOC-00854"
title: "Troubleshooting embedded dashboards"
doc_type: "product-docs"
section_path: "Dashboards > Embedded Dashboards > Troubleshooting embedded dashboards"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2025-01-20"
related_error_codes: ["ERR-1147", "ERR-1210"]
---

# Troubleshooting embedded dashboards

This page explains how embedded dashboards works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

To enable embedded dashboards, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

Audit events for embedded dashboards are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, embedded dashboards is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

When embedded dashboards is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: embedded dashboards performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.

### ERR-1210: PDF export failed: asset too large

Cause: Rendered dashboard exceeds the 50 MB export ceiling.

Resolution: Export tabs individually or lower image DPI in export settings.

This issue is fixed in version 5.1. Affected versions: 4.9, 5.0.
