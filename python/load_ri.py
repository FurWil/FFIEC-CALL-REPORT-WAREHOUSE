import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()


file_path = Path(
    "data/raw/FFIEC CDR Call Schedule RI 03312024.txt"
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


print("Reading FFIEC RI data...")


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


print(f"Rows loaded into pandas: {len(df):,}")
print(f"Columns loaded into pandas: {len(df.columns):,}")


with engine.begin() as connection:
    connection.execute(
        text("CREATE SCHEMA IF NOT EXISTS raw")
    )


print("Loading RI data into PostgreSQL...")


df.to_sql(
    name="ri_20240331",
    con=engine,
    schema="raw",
    if_exists="replace",
    index=False
)


print("Successfully loaded FFIEC RI data!")
print("PostgreSQL table: raw.ri_20240331")