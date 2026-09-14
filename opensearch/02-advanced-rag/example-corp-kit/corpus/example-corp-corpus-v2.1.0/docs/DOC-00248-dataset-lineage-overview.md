---
source_id: "DOC-00248"
title: "Dataset Lineage overview"
doc_type: "product-docs"
section_path: "Datasets > Dataset Lineage > Dataset Lineage overview"
product_area: "datasets"
product_version: "5.1"
acl: "public"
updated_at: "2025-03-05"
related_error_codes: ["ERR-3340"]
---

# Dataset Lineage overview

This page explains how dataset lineage works in Example Corp BI Platform and how to configure it for production workloads.

## Configuration

If your organization uses SAML SSO, dataset lineage inherits group membership from your identity provider on each login.

Audit events for dataset lineage are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

By default, dataset lineage is limited to 10 per workspace on the enterprise tier. Administrators can raise this limit from the admin console.

To enable dataset lineage, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

Performance tip: dataset lineage performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
