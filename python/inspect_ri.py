import pandas as pd

file_path = "data/raw/FFIEC CDR Call Schedule RI 03312024.txt"

df = pd.read_csv(
    file_path,
    sep="\t",
    header=0,
    skiprows=[1],
    dtype=str,
    na_filter=False
)

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head().to_string(index=False))
