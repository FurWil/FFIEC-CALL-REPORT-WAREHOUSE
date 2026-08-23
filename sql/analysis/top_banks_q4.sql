SELECT
    bank_id,
    bank_name,
    state,
    total_assets,
    total_liabilities,
    total_equity,
    net_income
FROM analytics.fct_bank_financials
WHERE report_date = DATE '2024-12-31'
  AND total_assets IS NOT NULL
ORDER BY total_assets DESC
LIMIT 25;

