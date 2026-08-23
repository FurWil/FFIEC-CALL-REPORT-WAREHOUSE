from datetime import datetime
from pathlib import Path
import zipfile


def get_quarter(reporting_period: str) -> str:
    """Convert YYYYMMDD into Q1/Q2/Q3/Q4."""

    month = reporting_period[4:6]

    quarter_map = {
        "03": "Q1",
        "06": "Q2",
        "09": "Q3",
        "12": "Q4",
    }

    if month not in quarter_map:
        raise ValueError(
            f"Unsupported reporting month: {month}. "
            "Expected 03, 06, 09, or 12."
        )

    return quarter_map[month]


def extract_call_report(reporting_period: str) -> None:
    """Extract the RC, POR, and RI files for a reporting period."""

    date_for_filename = datetime.strptime(
        reporting_period,
        "%Y%m%d"
    ).strftime("%m%d%Y")

    year = reporting_period[:4]
    quarter = get_quarter(reporting_period)

    zip_file = Path(
        f"data/raw/{year}/{quarter}/"
        f"FFIEC CDR Call Bulk All Schedules {date_for_filename}.zip"
    )

    output_folder = Path(
        f"data/raw/{year}/{quarter}"
    )

    if not zip_file.exists():
        raise FileNotFoundError(
            f"Could not find FFIEC ZIP file:\n{zip_file}"
        )

    files_to_extract = [
        f"FFIEC CDR Call Bulk POR {date_for_filename}.txt",
        f"FFIEC CDR Call Schedule RC {date_for_filename}.txt",
        f"FFIEC CDR Call Schedule RI {date_for_filename}.txt",
    ]

    with zipfile.ZipFile(zip_file, "r") as zip_ref:

        for file_name in files_to_extract:

            destination = output_folder / file_name

            if destination.exists():
                print(f"Already extracted: {file_name}")
                continue

            zip_ref.extract(
                file_name,
                output_folder
            )

            print(f"Extracted: {file_name}")


if __name__ == "__main__":
    extract_call_report("20240930")