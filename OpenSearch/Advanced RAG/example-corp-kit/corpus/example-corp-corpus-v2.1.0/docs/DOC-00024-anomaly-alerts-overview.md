---
source_id: "DOC-00024"
title: "Anomaly Alerts overview"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Anomaly Alerts > Anomaly Alerts overview"
product_area: "alerts"
product_version: "5.0"
acl: "public"
updated_at: "2025-11-12"
related_error_codes: ["ERR-4402"]
---

# Anomaly Alerts overview

Anomaly Alerts lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

To enable anomaly alerts, open the workspace settings panel and select the Alerts & Scheduled Reports tab. Changes apply within one refresh cycle and do not require a restart.

By default, anomaly alerts is limited to 100 per workspace on the standard tier. Administrators can raise this limit from the admin console.

Performance tip: anomaly alerts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When anomaly alerts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

If your organization uses SAML SSO, anomaly alerts inherits group membership from your identity provider on each login.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
