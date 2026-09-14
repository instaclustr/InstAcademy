---
source_id: "DOC-00216"
title: "How report bursting works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Report Bursting > How report bursting works"
product_area: "alerts"
product_version: "4.9"
acl: "public"
updated_at: "2025-11-08"
related_error_codes: ["ERR-4415", "ERR-4402"]
---

# How report bursting works

Report Bursting lets your team control who sees what without leaving Example Corp BI Platform.

## Configuration

When report bursting is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, report bursting is limited to 5 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable report bursting, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: report bursting performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, report bursting inherits group membership from your identity provider on each login.

## Common errors

### ERR-4415: Webhook signature mismatch

Cause: Receiving endpoint validated against a rotated webhook secret.

Resolution: Update the shared secret on the receiver; secrets rotate every 90 days by default.

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
