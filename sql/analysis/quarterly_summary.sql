SELECT
    report_date,
    COUNT(*) AS reporting_institutions,
    SUM(total_assets) AS aggregate_assets,
    SUM(total_liabilities) AS aggregate_liabilities,
    SUM(total_equity) AS aggregate_equity,
    SUM(net_income) AS aggregate_reported_net_income
FROM analytics.fct_bank_financials
GROUP BY report_date
ORDER BY report_date;

