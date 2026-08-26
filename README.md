# FFIEC Call Report Analytical Data Warehouse

## 1. Overview

This project builds a small analytical data warehouse from publicly available **FFIEC Call Report bulk data**.

The project demonstrates an end-to-end data engineering and analytics workflow:


FFIEC Central Data Repository
            ↓
      Python ingestion
            ↓
     PostgreSQL raw layer
            ↓
        dbt staging
            ↓
   Analytical fact table
            ↓
      SQL analysis


The pipeline is designed to be period-agnostic. A user supplies a Call Report quarter-end date, and the pipeline automatically loads that quarter plus the three preceding quarters.

For example:

```bash
python python/pipeline.py 2025-06-30
```

automatically creates a four-quarter window:


2024-09-30
2024-12-31
2025-03-31
2025-06-30


The same workflow can be used with other supported FFIEC quarter-end dates.


## 2. Project Goals

This project was designed to demonstrate:

* Automated ingestion of publicly available financial data
* Separation of raw ingestion from analytical transformation
* Relational data warehouse design
* Multi-period financial analysis
* Data-quality testing
* Reproducible local development
* Parameterized ingestion
* Idempotent data loading
* Reusable analytical SQL

---

## 3. Architecture

```text
                    FFIEC Central Data Repository
                                  |
                                  v
                           Python Pipeline
                                  |
                +-----------------+-----------------+
                |                 |                 |
                v                 v                 v
               POR               RC                RI
         Institution Info    Balance Sheet     Income Statement
                |                 |                 |
                +-----------------+-----------------+
                                  |
                                  v
                              PostgreSQL
                               raw schema
                                  |
                +-----------------+-----------------+
                |                 |                 |
                v                 v                 v
             raw.por            raw.rc            raw.ri
                |                 |                 |
                +-----------------+-----------------+
                                  |
                                  v
                                dbt
                                  |
                +-----------------+-----------------+
                |                 |                 |
                v                 v                 v
             stg_por            stg_rc            stg_ri
                \                 |                 /
                 \                |                /
                  +---------------+---------------+
                                  |
                                  v
                       fct_bank_financials
                                  |
                                  v
                           SQL analysis
```

---

## 4. Technology Stack

* **Python** — downloading, extraction, parsing, and data loading
* **pandas** — parsing FFIEC text files
* **PostgreSQL** — raw and analytical data storage
* **Docker** — reproducible PostgreSQL environment
* **dbt** — SQL transformations and data-quality testing
* **SQL** — analytical queries
* **Git/GitHub** — source control and reproducibility

---

## 5. Data Source and Scope

The project uses publicly available FFIEC Call Report bulk data from the:

**FFIEC Central Data Repository**

https://cdr.ffiec.gov/public/pws/downloadbulkdata.aspx

### Data Sources

The project currently uses three Call Report sources.

### POR — Panel of Reporters

Used for institution-level information such as:

* IDRSSD
* FDIC certificate number
* Financial institution name
* Address
* City
* State
* ZIP code

### RC — Balance Sheet

Used for:

* Total assets
* Total liabilities
* Total equity

### RI — Income Statement

Used for:

* Net income

Together, these sources provide enough information to demonstrate a complete ingestion, warehouse, transformation, and analytical workflow without loading every available Call Report schedule.

### Reporting Period Scope

The pipeline supports the four quarterly Call Report reporting dates:

* March 31
* June 30
* September 30
* December 31

The user supplies the **ending reporting period**, and the pipeline automatically calculates the preceding three quarters.

For example:

```bash
python python/pipeline.py 2025-06-30
```

loads:

```text
2024-09-30
2024-12-31
2025-03-31
2025-06-30
```

The exact four-quarter window changes automatically based on the date supplied.

---

## 6. Reproducing the Pipeline

### Prerequisites

Before setting up the project, install the following:

- Git
- Python 3.12+
- Docker with WSL 2 installed

Docker Desktop provides the PostgreSQL environment used by the project.

After installing Docker Desktop, start Docker Desktop and verify that
the Docker Engine is running:

```bash
docker info

### 6.1 Clone the Repository

```bash
git clone <repository-url>
cd FFIEC-CALL-REPORT-WAREHOUSE
```

### 6.2 Configure Environment Variables

Create a local environment file from the example:

```bash
cp .env.example .env
```

Update the PostgreSQL settings in `.env`.

**Do not commit `.env` to Git.**

The repository uses `.env.example` so that another user can provide their own local database configuration without exposing credentials.

### 6.3 Start PostgreSQL with Docker

Make sure Docker Desktop is running, then run:

```bash
docker compose up -d
```

Verify the container is running:

```bash
docker ps
```

### 6.4 Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 6.5 Load a Four-Quarter Window

Supply the desired ending FFIEC quarter-end date:

```bash
python python/pipeline.py 2025-06-30
```

Replace `2025-06-30` with **any supported FFIEC quarter-end date**.

For example:

```text
Input:
2025-06-30

Automatically loaded:
2024-09-30
2024-12-31
2025-03-31
2025-06-30
```

No Python source files need to be edited to change the reporting period.

### 6.6 Run dbt

Move into the dbt project:

```bash
cd dbt
```

Run the transformations:

```bash
dbt run
```

Run the data-quality tests:

```bash
dbt test
```

A successful test run should finish with:

```text
ERROR=0
```

---

## 7. Running the Analysis

The SQL files under `sql/analysis/` are standalone, read-only analytical queries. They run against the PostgreSQL warehouse and do not modify the database.

To move back into the FFIEC-CALL-REPORT-WAREHOUSE directory run the following command:

```bash
cd ..
```

Before running the analysis commands, load the PostgreSQL environment variables from `.env` into your shell:

```bash
set -a
source .env
set +a
```

The available analyses are described below.

### 7.1 Quarterly Summary

Run:

```bash
docker exec -i ffiec-postgres psql \
  -U "$POSTGRES_USER" \
  -d "$POSTGRES_DB" \
  < sql/analysis/quarterly_summary.sql
```

This provides a quarter-by-quarter summary of:

* Reporting institutions
* Aggregate assets
* Aggregate liabilities
* Aggregate equity
* Aggregate reported net income

The results cover the reporting periods currently loaded into `analytics.fct_bank_financials`.

### 7.2 Latest-Period Asset Growth

Run:

```bash
docker exec -i ffiec-postgres psql \
  -U "$POSTGRES_USER" \
  -d "$POSTGRES_DB" \
  < sql/analysis/asset_growth_latest_period.sql
```

This compares the latest loaded reporting period with the immediately preceding reporting period and calculates asset growth.

The query determines the latest available reporting date dynamically, so it does not depend on a specific year or quarter.

### 7.3 Top Five Latest-Quarter Four-Quarter Trend

Run:

```bash
docker exec -i ffiec-postgres psql \
  -U "$POSTGRES_USER" \
  -d "$POSTGRES_DB" \
  < sql/analysis/top_5_latest_quarter_four_quarter_trends.sql
```

This analysis:

1. Identifies the five largest institutions by total assets in the latest loaded quarter.
2. Selects those same five institutions as the analysis cohort.
3. Follows the cohort across the latest four reporting periods.
4. Calculates quarter-over-quarter asset and equity growth.
5. Reports net income and absolute asset changes.

The output contains:

```text
bank_name
report_date
total_assets
asset_growth_pct
total_equity
equity_growth_pct
net_income
asset_change
```

Because the analysis dynamically identifies the latest reporting period, it is not tied to a specific calendar year.

### 7.4 Top-Five Asset Concentration

Run:

```bash
docker exec -i ffiec-postgres psql \
  -U "$POSTGRES_USER" \
  -d "$POSTGRES_DB" \
  < sql/analysis/top_5_asset_concentration.sql
```

This is the primary analytical finding for the project.

The analysis:

1. Identifies the five largest institutions by total assets in the latest loaded quarter.
2. Holds that five-bank cohort constant across the latest four reporting periods.
3. Calculates total assets held by those five institutions.
4. Calculates total reported assets across the analytical population.
5. Calculates the five-bank share of total reported assets.
6. Measures the quarter-over-quarter change in that concentration.

The resulting output includes:

```text
report_date
top_5_assets
total_banking_assets
top_5_asset_share_pct
quarter_change_pct_points
```

This analysis is intended to answer:

> **How concentrated are reported banking assets among the five largest institutions, and how has that concentration changed over the latest four quarters?**

For the current loaded data, the five largest institutions as of the latest reporting period are:

* JPMorgan Chase Bank, N.A.
* Bank of America, N.A.
* Citibank, N.A.
* Wells Fargo Bank, N.A.
* Goldman Sachs Bank USA

The analysis is fully dynamic and will automatically use a different five-bank cohort if a different reporting window is loaded.


## 8. Warehouse Design

### Raw Layer

The raw schema contains:

```text
raw.rc
raw.por
raw.ri
```

Each table contains multiple reporting periods and includes a `report_date` column.

For example:

```text
raw.rc

IDRSSD | report_date | ...
-------+-------------+-----
37     | 2024-12-31  | ...
37     | 2025-03-31  | ...
37     | 2025-06-30  | ...
```

The raw layer is intentionally kept close to the structure of the FFIEC source data.

### dbt Staging Layer

dbt transforms the raw source tables into:

```text
stg_rc
stg_por
stg_ri
```

These models provide analyst-friendly column names and standardized data types.

### Analytical Fact Table

The primary analytical model is:

```text
analytics.fct_bank_financials
```

The intended grain is:

> **One row per financial institution per reporting period.**

The warehouse grain is therefore represented by:

```text
bank_id + report_date
```

The fact table contains:

```text
bank_id
report_date
bank_name
fdic_certificate
address
city
state
zip_code
total_assets
total_liabilities
total_equity
net_income
```

This allows multiple reporting periods for the same bank to coexist in one analytical table.

Example:

```text
JPMorgan | 2024-12-31 | ...
JPMorgan | 2025-03-31 | ...
JPMorgan | 2025-06-30 | ...
JPMorgan | 2025-09-30 | ...
```

---

## 9. Python Pipeline Components

### `pipeline.py`

Main entry point for the ingestion workflow.

Responsibilities:

1. Validate the reporting date
2. Calculate the rolling four-quarter window
3. Download required FFIEC files
4. Extract required schedules
5. Load raw data into PostgreSQL
6. Skip already-loaded reporting periods

### `download.py`

Downloads the FFIEC Call Report bulk ZIP for a requested reporting period.

### `extract.py`

Extracts POR, RC, and RI from the downloaded ZIP.

### `load_rc.py`

Loads Schedule RC into `raw.rc`.

### `load_por.py`

Loads POR into `raw.por`.

### `load_ri.py`

Loads Schedule RI into `raw.ri`.

---

## 10. Data Quality

The project uses dbt tests to enforce basic warehouse quality.

Tests include:

* `bank_id` must not be null
* `report_date` must not be null
* `bank_id + report_date` must be unique
* The fact table must maintain the intended grain

Run:

```bash
cd dbt
dbt test
```

A successful run should finish with:

```text
ERROR=0
```

---

## 11. Idempotent Ingestion

The ingestion pipeline is designed to be safely rerunnable.

Before processing a reporting period, the pipeline checks whether that period already exists in the raw PostgreSQL tables.

If the period has already been loaded, the corresponding ingestion steps are skipped.

For example:

```bash
python python/pipeline.py 2025-09-30
```

can be safely rerun after the data has already been loaded.

This prevents intentional duplicate ingestion and makes the pipeline more robust for repeated use.

---

## 12. Security and Reproducibility

Database credentials are stored locally in `.env` and are not committed to Git.

The repository includes `.env.example` so another user can create their own environment configuration.

Raw FFIEC ZIP and text files are excluded from Git because they can be regenerated through the parameterized ingestion pipeline.

---
## 13. Example Analytical Questions

The warehouse can answer questions such as:

* Which institutions have the largest balance sheets?
* Which banks experienced the largest recent asset growth?
* How has bank equity changed across reporting periods?
* How have aggregate bank assets changed over time?
* How have the largest institutions changed across the latest four quarters?


---

## 14. Limitations

This project intentionally uses a subset of the available FFIEC Call Report schedules.

It is designed to demonstrate:

* Data ingestion
* Relational storage
* Transformation
* Data-quality testing
* Warehouse grain design
* Longitudinal analysis

Call Report financial amounts are reported according to the units and reporting conventions of the source schedules. Selected monetary fields are converted to dollars in the dbt staging layer.

Income-statement values should be interpreted according to Call Report reporting conventions rather than automatically assumed to represent an isolated quarterly income statement.

---
