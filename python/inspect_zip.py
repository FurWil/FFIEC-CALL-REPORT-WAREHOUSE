import zipfile


zip_file = "data/raw/FFIEC CDR Call Bulk XBRL 03312024.zip"


with zipfile.ZipFile(zip_file, "r") as zip_ref:

    print("Files inside the ZIP:")

    for file in zip_ref.namelist():
        print(file)
