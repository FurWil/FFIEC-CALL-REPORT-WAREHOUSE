
WITH latest_quarter AS (
    SELECT
        MAX(report_date) AS report_date
    FROM analytics.fct_bank_financials
)

SELECT
    ROW_NUMBER() OVER (
        ORDER BY f.total_assets DESC
    ) AS rank,
    f.bank_name,
    f.total_assets
FROM analytics.fct_bank_financials AS f
INNER JOIN latest_quarter AS lq
    ON f.report_date = lq.report_date
WHERE f.total_assets IS NOT NULL
ORDER BY f.total_assets DESC
LIMIT 10;


-- ============================================================
-- 2. Aggregate asset concentration across latest 4 quarters
-- ============================================================

WITH latest_quarter AS (
    SELECT
        MAX(report_date) AS report_date
    FROM analytics.fct_bank_financials
),

top_10_banks AS (
    SELECT
        f.bank_id
    FROM analytics.fct_bank_financials AS f
    INNER JOIN latest_quarter AS lq
        ON f.report_date = lq.report_date
    WHERE f.total_assets IS NOT NULL
    ORDER BY f.total_assets DESC
    LIMIT 10
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

top_10_totals AS (
    SELECT
        f.report_date,
        SUM(f.total_assets) AS top_10_assets
    FROM analytics.fct_bank_financials AS f
    INNER JOIN top_10_banks AS t
        ON f.bank_id = t.bank_id
    INNER JOIN latest_four_quarters AS q
        ON f.report_date = q.report_date
    WHERE f.total_assets IS NOT NULL
    GROUP BY f.report_date
)

SELECT
    q.report_date,
    t.top_10_assets,
    q.total_banking_assets,

    ROUND(
        (
            t.top_10_assets
            / NULLIF(q.total_banking_assets, 0)
        ) * 100,
        2
    ) AS top_10_asset_share_pct,

    ROUND(
        (
            (
                t.top_10_assets
                / NULLIF(q.total_banking_assets, 0)
            )
            -
            LAG(
                t.top_10_assets
                / NULLIF(q.total_banking_assets, 0)
            ) OVER (
                ORDER BY q.report_date
            )
        ) * 100,
        2
    ) AS quarter_change_pct_points

FROM quarterly_totals AS q
INNER JOIN top_10_totals AS t
    ON q.report_date = t.report_date

ORDER BY q.report_date;
