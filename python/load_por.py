import os
from pathlib import Path
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()


def load_por(reporting_period: str) -> None:

    date_for_filename = datetime.strptime(
        reporting_period,
        "%Y%m%d"
    ).strftime("%m%d%Y")

    year = reporting_period[:4]
    month = reporting_period[4:6]

    quarter = {
        "03": "Q1",
        "06": "Q2",
        "09": "Q3",
        "12": "Q4",
    }[month]

    file_path = Path(
        f"data/raw/{year}/{quarter}/"
        f"FFIEC CDR Call Bulk POR {date_for_filename}.txt"
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

    print(f"Reading POR data for {reporting_period}...")

    df = pd.read_csv(
        file_path,
        sep="\t",
        header=0,
        dtype=str,
        na_filter=False
    )

    df.columns = [
        column.strip()
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        for column in df.columns
    ]

    df["report_date"] = pd.to_datetime(
        reporting_period,
        format="%Y%m%d"
    )

    print(f"Rows: {len(df):,}")

    with engine.begin() as connection:
        connection.execute(
            text("CREATE SCHEMA IF NOT EXISTS raw")
        )

    df.to_sql(
        name="por",
        con=engine,
        schema="raw",
        if_exists="append",
        index=False
    )

    print(f"Loaded POR data for {reporting_period}")