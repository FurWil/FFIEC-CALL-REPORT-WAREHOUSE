SELECT
    idrssd AS bank_id,

    report_date::date AS report_date,

    NULLIF(rcfd2170, '')::numeric * 1000 AS total_assets,

    NULLIF(rcfd2948, '')::numeric * 1000 AS total_liabilities,

    NULLIF(rcfd3210, '')::numeric * 1000 AS total_equity

FROM {{ source('ffiec_raw', 'rc') }}