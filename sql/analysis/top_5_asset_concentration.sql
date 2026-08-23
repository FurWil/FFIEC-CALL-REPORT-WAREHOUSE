WITH latest_quarter AS (
    SELECT
        MAX(report_date) AS report_date
    FROM analytics.fct_bank_financials
),

top_5_banks AS (
    SELECT
        f.bank_id
    FROM analytics.fct_bank_financials AS f
    INNER JOIN latest_quarter AS lq
        ON f.report_date = lq.report_date
    WHERE f.total_assets IS NOT NULL
    ORDER BY f.total_assets DESC
    LIMIT 5
),

latest_four_quarters AS (
    SELECT DISTINCT
        report_date
    FROM analytics.fct_bank_financials
    ORDER BY report_date DESC
    LIMIT 4
),

quarterly_totals AS (
    SELECT
        f.report_date,
        SUM(f.total_assets) AS total_banking_assets
    FROM analytics.fct_bank_financials AS f
    INNER JOIN latest_four_quarters AS q
        ON f.report_date = q.report_date
    WHERE f.total_assets IS NOT NULL
    GROUP BY f.report_date
),

top_5_totals AS (
    SELECT
        f.report_date,
        SUM(f.total_assets) AS top_5_assets
    FROM analytics.fct_bank_financials AS f
    INNER JOIN top_5_banks AS t
        ON f.bank_id = t.bank_id
    INNER JOIN latest_four_quarters AS q
        ON f.report_date = q.report_date
    WHERE f.total_assets IS NOT NULL
    GROUP BY f.report_date
),

concentration AS (
    SELECT
        q.report_date,
        q.total_banking_assets,
        t.top_5_assets,

        t.top_5_assets
            / NULLIF(q.total_banking_assets, 0)
            AS top_5_asset_share

    FROM quarterly_totals AS q
    INNER JOIN top_5_totals AS t
        ON q.report_date = t.report_date
)

SELECT
    report_date,
    top_5_assets,
    total_banking_assets,
    top_5_asset_share,

    top_5_asset_share
        - LAG(top_5_asset_share) OVER (
            ORDER BY report_date
        ) AS quarter_change

FROM concentration

ORDER BY report_date;
