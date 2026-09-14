---
source_id: "DOC-00683"
title: "How email delivery works"
doc_type: "product-docs"
section_path: "Alerts & Scheduled Reports > Email Delivery > How email delivery works"
product_area: "alerts"
product_version: "4.8"
acl: "public"
updated_at: "2025-11-21"
related_error_codes: ["ERR-4402"]
---

# How email delivery works

This page explains how email delivery works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

Performance tip: email delivery performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, email delivery inherits group membership from your identity provider on each login.

When email delivery is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

By default, email delivery is limited to 25 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

Audit events for email delivery are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-4402: Alert delivery throttled

Cause: More than 100 alert emails to a single recipient within one hour.

Resolution: Consolidate alerts with report bursting or raise the throttle limit per workspace.
