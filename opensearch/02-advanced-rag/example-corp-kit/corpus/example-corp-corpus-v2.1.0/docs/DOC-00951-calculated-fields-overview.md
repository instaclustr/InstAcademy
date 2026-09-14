---
source_id: "DOC-00951"
title: "Calculated Fields overview"
doc_type: "product-docs"
section_path: "Datasets > Calculated Fields > Calculated Fields overview"
product_area: "datasets"
product_version: "4.8"
acl: "public"
updated_at: "2025-01-03"
related_error_codes: ["ERR-3340"]
---

# Calculated Fields overview

Calculated Fields is available on version 4.8 and later. This guide covers setup, limits, and common failure modes.

## Configuration

By default, calculated fields is limited to 5 per workspace on the professional tier. Administrators can raise this limit from the admin console.

When calculated fields is combined with row-level security, evaluation happens before aggregation. Plan calculated fields accordingly.

Performance tip: calculated fields performs best when the underlying dataset uses incremental refresh. Full refreshes invalidate the associated cache.

Audit events for calculated fields are written to the workspace audit log within 60 seconds and retained for 13 months on the enterprise tier.

To enable calculated fields, open the workspace settings panel and select the Datasets tab. Changes apply within one refresh cycle and do not require a restart.

## Common errors

### ERR-3340: Row-level security rule not applied

Cause: RLS rules referencing calculated fields are evaluated after aggregation.

Resolution: Rewrite the RLS rule against a raw column, not a calculated field.
