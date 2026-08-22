
-- Use the `ref` function to select from other models

SELECT
    idrssd AS bank_id,

    NULLIF(rcfd2170, '')::numeric AS total_assets,

    NULLIF(rcfd2948, '')::numeric AS total_liabilities,

    NULLIF(rcfd3210, '')::numeric AS total_equity

FROM raw.rc_20240331