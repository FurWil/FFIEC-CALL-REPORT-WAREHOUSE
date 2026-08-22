import zipfile


zip_file = "data/raw/FFIEC CDR Call Bulk All Schedules 03312024.zip"


with zipfile.ZipFile(zip_file, "r") as zip_ref:

    print("Files inside the ZIP:\n")

    for file in zip_ref.namelist():
        print(file)
