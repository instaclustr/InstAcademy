---
source_id: "DOC-00715"
title: "Incremental Refresh overview"
doc_type: "product-docs"
section_path: "Datasets > Incremental Refresh > Incremental Refresh overview"
product_area: "datasets"
product_version: "5.1"
acl: "enterprise"
updated_at: "2026-06-06"
related_error_codes: ["ERR-3340"]
---

# Incremental Refresh overview

Incremental Refresh is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, incremental refresh inherits group membership from your identity provider on each login.

To enable incremental refresh, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: incremental refresh performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When incremental refresh is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for incremental refresh are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
