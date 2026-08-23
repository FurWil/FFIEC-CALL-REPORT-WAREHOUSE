SELECT
    bank_id,
    report_date,
    COUNT(*) AS row_count

FROM {{ ref('fct_bank_financials') }}

GROUP BY
    bank_id,
    report_date

HAVING COUNT(*) > 1
