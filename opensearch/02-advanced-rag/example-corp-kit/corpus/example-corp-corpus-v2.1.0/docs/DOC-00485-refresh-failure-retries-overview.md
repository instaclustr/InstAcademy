---
source_id: "DOC-00485"
title: "Refresh Failure Retries overview"
doc_type: "product-docs"
section_path: "Datasets > Refresh Failure Retries > Refresh Failure Retries overview"
product_area: "datasets"
product_version: "5.0"
acl: "public"
updated_at: "2024-02-23"
related_error_codes: ["ERR-3340"]
---

# Refresh Failure Retries overview

Refresh Failure Retries is available on version 5.0 and later. This guide covers setup, limits, and common failure modes.

## Configuration

To enable refresh failure retries, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: refresh failure retries performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

If your organization uses SAML SSO, refresh failure retries inherits group membership from your identity provider on each login.

Audit events for refresh failure retries are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

When refresh failure retries is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
