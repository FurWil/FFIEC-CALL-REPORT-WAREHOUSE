import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# Load database settings from .env
load_dotenv()


# Location of the POR file
file_path = Path(
    "data/raw/FFIEC CDR Call Bulk POR 03312024.txt"
)


# Build PostgreSQL connection string
database_url = (
    f"postgresql+psycopg://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)


# Connect to PostgreSQL
engine = create_engine(database_url)


print("Reading FFIEC POR data...")


# POR has column names in the first row
df = pd.read_csv(
    file_path,
    sep="\t",
    header=0,
    dtype=str,
    na_filter=False
)


# Clean up the column names
df.columns = [
    column.strip()
    .lower()
    .replace(" ", "_")
    .replace("/", "_")
    for column in df.columns
]


print(f"Rows loaded into pandas: {len(df):,}")
print(f"Columns loaded into pandas: {len(df.columns):,}")


# Make sure the raw schema exists
with engine.begin() as connection:
    connection.execute(
        text("CREATE SCHEMA IF NOT EXISTS raw")
    )


print("Loading POR data into PostgreSQL...")


# Create/replace the PostgreSQL table
df.to_sql(
    name="por_20240331",
    con=engine,
    schema="raw",
    if_exists="replace",
    index=False
)


print("Successfully loaded FFIEC POR data!")
print("PostgreSQL table: raw.por_20240331")