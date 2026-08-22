import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


# Load our database settings from .env
load_dotenv()


# Location of the FFIEC RC file
file_path = Path(
    "data/raw/FFIEC CDR Call Schedule RC 03312024.txt"
)


# Build the PostgreSQL connection string
database_url = (
    f"postgresql+psycopg://"
    f"{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)


# Create a connection to PostgreSQL
engine = create_engine(database_url)


print("Reading FFIEC data...")

# Read the FFIEC file.
#
# Row 1 = FFIEC field codes
# Row 2 = human-readable descriptions
# Row 3 onward = actual bank data
#
# We want row 1 as our column names and skip row 2.
df = pd.read_csv(
    file_path,
    sep="\t",
    header=0,
    skiprows=[1],
    dtype=str,
    na_filter=False
)


# Clean up column names slightly
df.columns = [column.strip().lower() for column in df.columns]


print(f"Rows loaded into pandas: {len(df):,}")
print(f"Columns loaded into pandas: {len(df.columns):,}")


# Create the raw schema if it doesn't exist
with engine.begin() as connection:
    connection.execute(
        text("CREATE SCHEMA IF NOT EXISTS raw")
    )


print("Loading data into PostgreSQL...")

# Load the data into PostgreSQL
df.to_sql(
    name="rc_20240331",
    con=engine,
    schema="raw",
    if_exists="replace",
    index=False
)


print("Successfully loaded FFIEC RC data!")
print("PostgreSQL table: raw.rc_20240331")