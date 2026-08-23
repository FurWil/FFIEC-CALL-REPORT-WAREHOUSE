WITH bank_periods AS (
    SELECT
        bank_id,
        bank_name,
        state,
        report_date,
        total_assets,
        LAG(total_assets) OVER (
            PARTITION BY bank_id
            ORDER BY report_date
        ) AS prior_assets
    FROM analytics.fct_bank_financials
),

q4_growth AS (
    SELECT
        bank_id,
        bank_name,
        state,
        total_assets AS q4_assets,
        prior_assets AS q3_assets,
        total_assets - prior_assets AS asset_change,
        (total_assets - prior_assets)
            / NULLIF(prior_assets, 0) AS asset_growth_pct
    FROM bank_periods
    WHERE report_date = DATE '2024-12-31'
)

SELECT *
FROM q4_growth
WHERE prior_assets IS NOT NULL
ORDER BY asset_growth_pct DESC
LIMIT 20;

