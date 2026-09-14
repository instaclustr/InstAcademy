---
source_id: "DOC-00483"
title: "Dataset Lineage overview"
doc_type: "product-docs"
section_path: "Datasets > Dataset Lineage > Dataset Lineage overview"
product_area: "datasets"
product_version: "5.1"
acl: "public"
updated_at: "2025-06-05"
related_error_codes: ["ERR-3340"]
---

# Dataset Lineage overview

Dataset Lineage is available on version 5.1 and later. This guide covers setup, limits, and common failure modes.

## Configuration

If your organization uses SAML SSO, dataset lineage inherits group membership from your identity provider on each login.

Performance tip: dataset lineage performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

When dataset lineage is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Audit events for dataset lineage are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable dataset lineage, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
