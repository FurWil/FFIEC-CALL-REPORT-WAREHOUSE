SELECT
    rc.bank_id,

    por.bank_name,
    por.fdic_certificate,
    por.address,
    por.city,
    por.state,
    por.zip_code,

    rc.total_assets,
    rc.total_liabilities,
    rc.total_equity,

    ri.net_income,

    ri.net_income / NULLIF(rc.total_assets, 0) AS roa

FROM {{ ref('stg_rc_20240331') }} AS rc

LEFT JOIN {{ ref('stg_por_20240331') }} AS por
    ON rc.bank_id = por.bank_id

LEFT JOIN {{ ref('stg_ri_20240331') }} AS ri
    ON rc.bank_id = ri.bank_id
