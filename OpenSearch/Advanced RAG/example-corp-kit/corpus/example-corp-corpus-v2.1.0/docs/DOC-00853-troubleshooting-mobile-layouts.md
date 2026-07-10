---
source_id: "DOC-00853"
title: "Troubleshooting mobile layouts"
doc_type: "product-docs"
section_path: "Dashboards > Mobile Layouts > Troubleshooting mobile layouts"
product_area: "dashboards"
product_version: "4.8"
acl: "standard"
updated_at: "2025-12-04"
related_error_codes: ["ERR-1147"]
---

# Troubleshooting mobile layouts

This page explains how mobile layouts works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, mobile layouts inherits group membership from your identity provider on each login.

Performance tip: mobile layouts performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When mobile layouts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

To enable mobile layouts, open the workspace settings panel and select the Dashboards tab. Changes apply within one refresh cycle and do not require a restart.

By default, mobile layouts is limited to 100 per workspace on the professional tier. Administrators can raise this limit from the admin console.

## Common errors

### ERR-1147: Cross-filter loop detected

Cause: Two widgets reference each other as filter sources.

Resolution: Remove one direction of the cross-filter relationship.
