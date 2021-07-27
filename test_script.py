
import file_merger.file_merger as fm
import pandas as pd

fm.generic()

cue_sheet = "data/TOO LARGE JENNIFER CUE SHEETS 106 MU.xls"

df = pd.read_excel(cue_sheet, skiprows=15)

print(df.head())
print(len(df))

df.dropna(how="any", inplace=True)

print(len(df))
new_columns = [x.strip() for x in df.columns.tolist()]

df.columns = new_columns
print(df.columns.tolist())


