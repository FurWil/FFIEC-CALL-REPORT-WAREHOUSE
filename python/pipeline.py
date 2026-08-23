import os
import sys
from datetime import datetime

import psycopg
from dotenv import load_dotenv

from download import download_call_report
from extract import extract_call_report
from load_rc import load_rc
from load_por import load_por
from load_ri import load_ri


load_dotenv()


def already_loaded(reporting_period: str) -> bool:
    """
    Check whether this reporting period already exists
    in the raw RC table.
    """

    connection = psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM raw.rc
                    WHERE report_date = %s
                )
                """,
                (
                    datetime.strptime(
                        reporting_period,
                        "%Y%m%d"
                    ).date(),
                ),
            )

            return cursor.fetchone()[0]

    finally:
        connection.close()


def main():

    if len(sys.argv) != 2:
        print(
            "Usage: python python/pipeline.py YYYY-MM-DD"
        )
        sys.exit(1)

    user_date = sys.argv[1]

    try:
        reporting_period = datetime.strptime(
            user_date,
            "%Y-%m-%d"
        ).strftime("%Y%m%d")

    except ValueError:
        print(
            "Invalid date. Use YYYY-MM-DD, "
            "for example: 2024-09-30"
        )
        sys.exit(1)

    print(
        f"\nStarting FFIEC pipeline for {user_date}\n"
    )

    # Stop if this reporting period has already been loaded.
    if already_loaded(reporting_period):
        print(
            f"Reporting period {user_date} is already "
            "loaded into PostgreSQL."
        )
        print(
            "No data was changed."
        )
        sys.exit(0)

    # 1. Download
    download_call_report(reporting_period)

    # 2. Extract
    extract_call_report(reporting_period)

    # 3. Load raw data
    load_rc(reporting_period)
    load_por(reporting_period)
    load_ri(reporting_period)

    print(
        f"\nPipeline completed successfully for {user_date}!"
    )


if __name__ == "__main__":
    main()