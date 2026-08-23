from datetime import datetime
from pathlib import Path

from ffiec_data_collector import FFIECDownloader, Product, FileFormat


def download_call_report(reporting_period: str) -> Path:
    """
    Download the FFIEC All Schedules Call Report ZIP
    for a reporting period in YYYYMMDD format.
    """

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

    output_folder = Path(f"data/raw/{year}/{quarter}")
    output_folder.mkdir(parents=True, exist_ok=True)

    downloader = FFIECDownloader()

    print(f"Downloading FFIEC data for {reporting_period}...")

    result = downloader.download(
        product=Product.CALL_SINGLE,
        period=reporting_period,
        format=FileFormat.TSV
    )

    if not result.success:
        raise RuntimeError(
            f"FFIEC download failed: {result.error_message}"
        )

    downloaded_file = Path(result.file_path)

    destination = output_folder / (
        f"FFIEC CDR Call Bulk All Schedules {date_for_filename}.zip"
    )

    downloaded_file.replace(destination)

    print(f"Download successful: {destination}")

    return destination