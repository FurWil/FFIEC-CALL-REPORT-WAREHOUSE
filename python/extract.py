import zipfile
from pathlib import Path
from datetime import datetime


REPORTING_PERIOD = "20241231"

# Convert YYYYMMDD → MMDDYYYY for FFIEC filenames
date_for_filename = datetime.strptime(
    REPORTING_PERIOD,
    "%Y%m%d"
).strftime("%m%d%Y")

zip_file = Path(
    f"data/raw/2024/Q4/"
    f"FFIEC CDR Call Bulk All Schedules {date_for_filename}.zip"
)

output_folder = Path("data/raw/2024/Q4")


files_to_extract = [
    f"FFIEC CDR Call Bulk POR {date_for_filename}.txt",
    f"FFIEC CDR Call Schedule RC {date_for_filename}.txt",
    f"FFIEC CDR Call Schedule RI {date_for_filename}.txt",
]


with zipfile.ZipFile(zip_file, "r") as zip_ref:

    for file_name in files_to_extract:

        zip_ref.extract(
            file_name,
            output_folder
        )

        print(f"Extracted: {file_name}")