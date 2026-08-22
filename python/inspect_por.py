import pandas as pd

file_path = "data/raw/FFIEC CDR Call Bulk POR 03312024.txt"


df = pd.read_csv(
    file_path,
    sep="\t",
    header=None,
    dtype=str
)

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nFirst 5 rows:")
print(df.head().to_string(index=False, header=False))