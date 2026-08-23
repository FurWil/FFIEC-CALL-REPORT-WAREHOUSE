SELECT
    idrssd AS bank_id,

    report_date::date AS report_date,

    NULLIF(riad4340, '')::numeric * 1000 AS net_income

FROM {{ source('ffiec_raw', 'ri') }}