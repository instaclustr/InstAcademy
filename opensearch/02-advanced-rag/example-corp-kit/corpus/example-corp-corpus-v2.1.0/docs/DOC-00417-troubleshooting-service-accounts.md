---
source_id: "DOC-00417"
title: "Troubleshooting service accounts"
doc_type: "product-docs"
section_path: "REST API & Embedding > Service Accounts > Troubleshooting service accounts"
product_area: "api"
product_version: "4.8"
acl: "professional"
updated_at: "2024-08-18"
related_error_codes: ["ERR-6640"]
---

# Troubleshooting service accounts

Service Accounts lets your team act on data faster without leaving Example Corp BI Platform.

## Configuration

By default, service accounts is limited to 50 per workspace on the professional tier. Administrators can raise this limit from the admin console.

Audit events for service accounts are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable service accounts, open the workspace settings panel and select the REST API & Embedding tab. Changes apply within one refresh cycle and do not require a restart.

If your organization uses SAML SSO, service accounts inherits group membership from your identity provider on each login.

When service accounts is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-6640: Signed embed URL expired

Cause: Embed URLs are valid for 10 minutes; the host page cached one longer.

Resolution: Generate embed URLs server side per page load, never cache them.
