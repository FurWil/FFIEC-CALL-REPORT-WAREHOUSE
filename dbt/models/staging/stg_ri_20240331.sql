SELECT
    idrssd AS bank_id,

    NULLIF(riad4340, '')::numeric AS net_income

FROM raw.ri_20240331
