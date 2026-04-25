select
  opportunity_id,
  segment,
  stage,
  revenue_gap
from revenue_pipeline
where fiscal_year = 2026
  and opportunity_type = 'new_business';
