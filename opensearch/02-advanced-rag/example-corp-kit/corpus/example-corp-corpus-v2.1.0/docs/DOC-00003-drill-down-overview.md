---
source_id: "DOC-00003"
title: "Drill-Down overview"
doc_type: "product-docs"
section_path: "Dashboards > Drill-Down > Drill-Down overview"
product_area: "dashboards"
product_version: "5.1"
acl: "standard"
updated_at: "2026-04-11"
related_error_codes: ["ERR-1102", "ERR-1147"]
---

# Drill-Down overview

This page explains how drill-down works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Audit events for drill-down are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When drill-down is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, drill-down is limited to 5 per workspace on the standard tier. Administrators can raise this limit from the admin console.

If your organization uses SAML SSO, drill-down inherits group membership from your identity provider on each login.

To enable drill-down, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
