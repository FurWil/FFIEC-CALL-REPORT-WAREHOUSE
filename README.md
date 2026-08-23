# FFIEC Call Report Analytical Data Warehouse

## Overview

This project builds a small analytical data warehouse from publicly
available FFIEC Call Report bulk data.

The pipeline downloads, extracts, and loads FFIEC Call Report data
into PostgreSQL, then uses dbt to transform the raw data into an
analytical fact table.

### Scope

The ingestion pipeline is parameterized by reporting period and
automatically loads a rolling four-quarter window ending on the
quarter supplied by the user.

For example:

    python python/pipeline.py 2025-06-30

loads the following reporting periods:

- September 30, 2024
- December 31, 2024
- March 31, 2025
- June 30, 2025

This rolling four-quarter design supports longitudinal analysis while
keeping the demonstration dataset intentionally small enough to
reproduce locally.

The project currently focuses on three Call Report sources:

- POR — Panel of Reporters / institution information
- RC — balance sheet
- RI — income statement

## Reproducing the Pipeline

### 1. Clone the repository

    git clone <repository-url>

### 2. Configure environment variables

    cp .env.example .env

Update the PostgreSQL credentials in `.env`.

### 3. Start PostgreSQL

    docker compose up -d

### 4. Install Python dependencies

    pip install -r requirements.txt

### 5. Load a four-quarter reporting window

Supply the ending Call Report quarter-end date:

    python python/pipeline.py 2025-06-30

The pipeline automatically calculates the three preceding quarterly
reporting periods.

The accepted reporting dates are:

- March 31
- June 30
- September 30
- December 31

### 6. Run dbt

    cd dbt
    dbt run
    dbt test

The dbt layer transforms the raw FFIEC data into the analytical
`fct_bank_financials` model.

## Idempotent Ingestion

The ingestion pipeline checks whether each reporting period has
already been loaded into the raw PostgreSQL tables.

If a period is already present, the corresponding download and load
steps are skipped, preventing duplicate records when the pipeline is
rerun.

## Analysis

Example analytical queries are located in:

    sql/analysis/

These include:

- quarterly aggregate summaries
- year-end bank rankings
- asset-growth analysis

## Data Quality

dbt tests validate the analytical model's required fields and grain.

The intended grain is:

bank_id + report_date

## Data Source

FFIEC Central Data Repository Call Report bulk data.
https://cdr.ffiec.gov/public/pws/downloadbulkdata.aspx


Call Report financial amounts are provided in thousands of dollars in the source schedules; the dbt staging layer converts selected monetary fields to dollars. Income-statement values should be interpreted according to the reporting-period conventions of the Call Report rather than assumed to represent an isolated quarterly income statement.
