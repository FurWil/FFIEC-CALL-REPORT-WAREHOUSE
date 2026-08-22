import zipfile


zip_file = "data/raw/FFIEC CDR Call Bulk All Schedules 03312024.zip"

file_to_inspect = "FFIEC CDR Call Schedule RC 03312024.txt"


with zipfile.ZipFile(zip_file, "r") as zip_ref:

    with zip_ref.open(file_to_inspect) as file:

        for i in range(5):
            line = file.readline().decode("utf-8", errors="replace")
            print(line.rstrip())