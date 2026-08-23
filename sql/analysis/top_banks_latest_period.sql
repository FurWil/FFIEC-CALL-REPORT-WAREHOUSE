SELECT
    bank_id,
    bank_name,
    state,
    total_assets,
    total_liabilities,
    total_equity,
    net_income

FROM analytics.fct_bank_financials

WHERE report_date = (
    SELECT MAX(report_date)
    FROM analytics.fct_bank_financials
)

  AND total_assets IS NOT NULL

ORDER BY total_assets DESC

LIMIT 25;