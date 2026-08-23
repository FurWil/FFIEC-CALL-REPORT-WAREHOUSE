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

latest_period AS (

    SELECT
        MAX(report_date) AS report_date

    FROM analytics.fct_bank_financials

),

latest_growth AS (

    SELECT
        bp.bank_id,
        bp.bank_name,
        bp.state,

        bp.report_date,

        bp.total_assets AS current_assets,
        bp.prior_assets,

        bp.total_assets - bp.prior_assets AS asset_change,

        (
            bp.total_assets - bp.prior_assets
        ) / NULLIF(bp.prior_assets, 0) AS asset_growth_pct

    FROM bank_periods AS bp

    INNER JOIN latest_period AS lp
        ON bp.report_date = lp.report_date

    WHERE bp.prior_assets IS NOT NULL

)

SELECT
    bank_id,
    bank_name,
    state,
    report_date,
    current_assets,
    prior_assets,
    asset_change,
    asset_growth_pct

FROM latest_growth

ORDER BY asset_growth_pct DESC;