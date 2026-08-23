import os
from pathlib import Path
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()


REPORTING_PERIOD = "20241231"

date_for_filename = datetime.strptime(
    REPORTING_PERIOD,
    "%Y%m%d"
).strftime("%m%d%Y")

year = REPORTING_PERIOD[:4]
month = REPORTING_PERIOD[4:6]

quarter = {
    "03": "Q1",
    "06": "Q2",
    "09": "Q3",
    "12": "Q4",
}[month]

file_path = Path(
    f"data/raw/{year}/{quarter}/"
    f"FFIEC CDR Call Schedule RI {date_for_filename}.txt"
)


database_url = (
    f"postgresql+psycopg://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(database_url)

print(f"Reading RI data for {REPORTING_PERIOD}...")

df = pd.read_csv(
    file_path,
    sep="\t",
    header=0,
    skiprows=[1],
    dtype=str,
    na_filter=False
)

df.columns = [
    column.strip().lower()
    for column in df.columns
]

df["report_date"] = pd.to_datetime(
    REPORTING_PERIOD,
    format="%Y%m%d"
)

print(f"Rows loaded into pandas: {len(df):,}")
print(f"Columns loaded into pandas: {len(df.columns):,}")

with engine.begin() as connection:
    connection.execute(
        text("CREATE SCHEMA IF NOT EXISTS raw")
    )

print("Loading RI data into PostgreSQL...")

df.to_sql(
    name="ri",
    con=engine,
    schema="raw",
    if_exists="append",
    index=False
)

print(f"Successfully loaded raw.ri for {REPORTING_PERIOD}!")