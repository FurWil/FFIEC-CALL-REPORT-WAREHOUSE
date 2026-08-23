import os
import sys
from datetime import date, datetime

import psycopg
from dotenv import load_dotenv

from download import download_call_report
from extract import extract_call_report
from load_rc import load_rc
from load_por import load_por
from load_ri import load_ri


load_dotenv()


QUARTER_END_MONTHS = {
    3: 31,
    6: 30,
    9: 30,
    12: 31,
}


def validate_reporting_date(user_date: str) -> date:
    """Validate that the supplied date is a Call Report quarter-end date."""

    try:
        reporting_date = datetime.strptime(
            user_date,
            "%Y-%m-%d"
        ).date()
    except ValueError as exc:
        raise ValueError(
            "Invalid date. Use YYYY-MM-DD, for example 2024-09-30."
        ) from exc

    if (
        reporting_date.month not in QUARTER_END_MONTHS
        or reporting_date.day != QUARTER_END_MONTHS[reporting_date.month]
    ):
        raise ValueError(
            "The date must be a Call Report quarter-end date: "
            "March 31, June 30, September 30, or December 31."
        )

    return reporting_date


def previous_quarter(reporting_date: date) -> date:
    """Return the quarter immediately preceding a reporting date."""

    if reporting_date.month == 3:
        return date(reporting_date.year - 1, 12, 31)

    if reporting_date.month == 6:
        return date(reporting_date.year, 3, 31)

    if reporting_date.month == 9:
        return date(reporting_date.year, 6, 30)

    return date(reporting_date.year, 9, 30)


def get_reporting_periods(end_date: date, periods: int = 4) -> list[str]:
    """
    Return the requested number of quarter-end periods,
    oldest to newest, in YYYYMMDD format.
    """

    dates = []
    current_date = end_date

    for _ in range(periods):
        dates.append(current_date.strftime("%Y%m%d"))
        current_date = previous_quarter(current_date)

    dates.reverse()

    return dates


def period_has_rows(table_name: str, reporting_period: str) -> bool:
    """
    Check whether a raw table already contains rows for a reporting period.
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
                    FROM information_schema.tables
                    WHERE table_schema = 'raw'
                      AND table_name = %s
                )
                """,
                (table_name,),
            )

            table_exists = cursor.fetchone()[0]

            if not table_exists:
                return False

            cursor.execute(
                f"""
                SELECT EXISTS (
                    SELECT 1
                    FROM raw.{table_name}
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


def main() -> None:

    if len(sys.argv) != 2:
        print(
            "Usage: python python/pipeline.py YYYY-MM-DD"
        )
        sys.exit(1)

    try:
        end_date = validate_reporting_date(sys.argv[1])
    except ValueError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    reporting_periods = get_reporting_periods(end_date)

    print()
    print(
        f"FFIEC Call Report pipeline ending {end_date}"
    )
    print("Four-quarter window:")

    for period in reporting_periods:
        formatted = datetime.strptime(
            period,
            "%Y%m%d"
        ).strftime("%Y-%m-%d")

        print(f"  - {formatted}")

    print()

    for reporting_period in reporting_periods:

        formatted_date = datetime.strptime(
            reporting_period,
            "%Y%m%d"
        ).strftime("%Y-%m-%d")

        print("=" * 60)
        print(f"Processing {formatted_date}")
        print("=" * 60)

        # Download and extract once for this period.
        download_call_report(reporting_period)
        extract_call_report(reporting_period)

        # Load each source only if that source/period isn't already present.
        if period_has_rows("rc", reporting_period):
            print(f"RC already loaded for {formatted_date}.")
        else:
            load_rc(reporting_period)

        if period_has_rows("por", reporting_period):
            print(f"POR already loaded for {formatted_date}.")
        else:
            load_por(reporting_period)

        if period_has_rows("ri", reporting_period):
            print(f"RI already loaded for {formatted_date}.")
        else:
            load_ri(reporting_period)

        print()

    print("=" * 60)
    print("Pipeline completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()