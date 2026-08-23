SELECT
    idrssd AS bank_id,

    report_date::date AS report_date,

    NULLIF(riad4340, '')::numeric * 1000 AS net_income

FROM raw.ridocker exec -it ffiec-postgres psql -U furwil -d call_reports