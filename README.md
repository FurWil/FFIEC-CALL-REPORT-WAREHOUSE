# FFIEC Call Report Analytical Data Warehouse

## Overview

This project builds a small analytical data warehouse from publicly
available FFIEC Call Report bulk data.

The pipeline downloads, extracts, and loads FFIEC Call Report data
into PostgreSQL, then uses dbt to transform the raw data into an
analytical fact table.

## Scope

The project uses the four 2024 quarterly reporting periods:

- March 31, 2024
- June 30, 2024
- September 30, 2024
- December 31, 2024

The project focuses on three FFIEC schedules:

- POR — institution information
- RC — balance sheet
- RI — income statement

This scope was chosen to demonstrate a complete ingestion,
transformation, and analytical workflow without loading every
available Call Report schedule.

## Architecture

FFIEC CDR
    ↓
Python ingestion
    ↓
PostgreSQL raw schema
    ↓
dbt staging models
    ↓
fct_bank_financials
    ↓
SQL analysis

## Technology

- Python
- pandas
- PostgreSQL
- Docker
- dbt
- SQL
- GitHub

## Warehouse Grain

The primary analytical fact table has one row per:

bank_id + report_date

This allows multiple reporting periods for the same financial
institution.

## Raw Layer

The Python pipeline loads:

- raw.rc
- raw.por
- raw.ri

Each table contains a report_date column.

## dbt Layer

dbt creates:

- stg_rc
- stg_por
- stg_ri
- fct_bank_financials

The fact model combines institution information, balance-sheet
information, and income-statement information.

## Reproducing the Pipeline

Create the local environment file:

    cp .env.example .env

Start PostgreSQL:

    docker compose up -d

Install Python dependencies:

    pip install -r requirements.txt

Run ingestion for a reporting period:

    python python/pipeline.py 2024-09-30

Run dbt:

    cd dbt
    dbt run
    dbt test

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