SELECT
    rc.bank_id,
    rc.report_date,

    por.bank_name,
    por.fdic_certificate,
    por.address,
    por.city,
    por.state,
    por.zip_code,

    rc.total_assets,
    rc.total_liabilities,
    rc.total_equity,

    ri.net_income

FROM {{ ref('stg_rc') }} AS rc

LEFT JOIN {{ ref('stg_por') }} AS por
    ON rc.bank_id = por.bank_id
    AND rc.report_date = por.report_date

LEFT JOIN {{ ref('stg_ri') }} AS ri
    ON rc.bank_id = ri.bank_id
    AND rc.report_date = ri.report_date