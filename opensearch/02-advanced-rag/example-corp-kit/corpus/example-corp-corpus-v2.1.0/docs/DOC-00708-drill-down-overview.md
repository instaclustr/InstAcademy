---
source_id: "DOC-00708"
title: "Drill-Down overview"
doc_type: "product-docs"
section_path: "Dashboards > Drill-Down > Drill-Down overview"
product_area: "dashboards"
product_version: "5.0"
acl: "public"
updated_at: "2025-10-22"
related_error_codes: ["ERR-1102"]
---

# Drill-Down overview

This page explains how drill-down works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

When drill-down is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for drill-down are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

Performance tip: drill-down performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, drill-down inherits group membership from your identity provider on each login.

By default, drill-down is limited to 50 per workspace on the standard tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-1102: Dashboard render timeout

Cause: Widget query exceeded the 60 second render budget.

Resolution: Reduce widget count or enable result caching on the underlying dataset.

This issue is fixed in version 5.0. Affected versions: 4.8, 4.9.
