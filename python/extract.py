import zipfile
from pathlib import Path


zip_file = Path(
    "data/raw/FFIEC CDR Call Bulk All Schedules 03312024.zip"
)

output_folder = Path("data/raw")


file_to_extract = "FFIEC CDR Call Schedule RC 03312024.txt"


with zipfile.ZipFile(zip_file, "r") as zip_ref:

    zip_ref.extract(
        file_to_extract,
        output_folder
    )


print("RC file extracted successfully!")