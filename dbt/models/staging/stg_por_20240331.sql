SELECT
    idrssd AS bank_id,

    fdic_certificate_number AS fdic_certificate,

    financial_institution_name AS bank_name,

    financial_institution_address AS address,

    financial_institution_city AS city,

    financial_institution_state AS state,

    financial_institution_zip_code AS zip_code,

    financial_institution_filing_type AS filing_type,

    last_date_time_submission_updated_on AS submission_updated_at

FROM raw.por_20240331

