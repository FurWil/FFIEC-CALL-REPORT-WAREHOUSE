SELECT
    idrssd AS bank_id,

    report_date::date AS report_date,

    fdic_certificate_number AS fdic_certificate,

    financial_institution_name AS bank_name,

    financial_institution_address AS address,

    financial_institution_city AS city,

    financial_institution_state AS state,

    financial_institution_zip_code AS zip_code

FROM raw.por