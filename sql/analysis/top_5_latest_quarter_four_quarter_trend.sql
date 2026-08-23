WITH latest_quarter AS (
    SELECT
        MAX(report_date) AS report_date
    FROM analytics.fct_bank_financials
),

top_5_banks AS (
    SELECT
        f.bank_id,
        f.bank_name
    FROM analytics.fct_bank_financials AS f
    INNER JOIN latest_quarter AS lq
        ON f.report_date = lq.report_date
    WHERE f.total_assets IS NOT NULL
    ORDER BY f.total_assets DESC
    LIMIT 5
),

four_quarters AS (
    SELECT DISTINCT
        report_date
    FROM analytics.fct_bank_financials
    ORDER BY report_date DESC
    LIMIT 4
),

bank_quarters AS (
    SELECT
        b.bank_id,
        b.bank_name,
        q.report_date
    FROM top_5_banks AS b
    CROSS JOIN four_quarters AS q
),

metrics AS (
    SELECT
        bq.bank_id,
        bq.bank_name,
        bq.report_date,

        f.total_assets,
        f.total_equity,
        f.net_income,
        f.roa

    FROM bank_quarters AS bq

    LEFT JOIN analytics.fct_bank_financials AS f
        ON bq.bank_id = f.bank_id
        AND bq.report_date = f.report_date
),

with_changes AS (
    SELECT
        *,
        
        LAG(total_assets) OVER (
            PARTITION BY bank_id
            ORDER BY report_date
        ) AS prior_total_assets,

        LAG(total_equity) OVER (
            PARTITION BY bank_id
            ORDER BY report_date
        ) AS prior_total_equity

    FROM metrics
)

SELECT
    bank_name,
    report_date,
    total_assets,

    (
        total_assets - prior_total_assets
    ) / NULLIF(prior_total_assets, 0)
        AS asset_growth_pct,

    total_equity,

    (
        total_equity - prior_total_equity
    ) / NULLIF(prior_total_equity, 0)
        AS equity_growth_pct,

    net_income,
    roa,

    total_assets - prior_total_assets
        AS asset_change

FROM with_changes

ORDER BY
    bank_name,
    report_date;