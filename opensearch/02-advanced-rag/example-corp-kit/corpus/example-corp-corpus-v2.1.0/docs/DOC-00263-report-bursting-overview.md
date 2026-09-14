---
source_id: "DOC-00263"
title: "Report Bursting overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Report Bursting > Report Bursting overview"
product_area: "alerts"
product_version: "5.0"
acl: "public"
updated_at: "2025-08-04"
related_error_codes: ["ERR-4402"]
---

# Report Bursting overview

This page explains how report bursting works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: report bursting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for report bursting are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable report bursting, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

By default, report bursting is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

When report bursting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
