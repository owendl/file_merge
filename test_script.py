
import file_merger.file_merger as fm
import pandas as pd



fm.generic()

vendor_files = [
        {"vendor":"FTM","filename": "data/FTM-AA_COMPOSER-PUBLISHER_6-16-21.xlsx", "sheetname":"AA"}
        ,{"vendor":"AA","filename": "data/FTM-AA_COMPOSER-PUBLISHER_6-16-21.xlsx", "sheetname":"FTM"}
        ,{"vendor":"SignatureTracks","filename": "data/Signature Tracks - Composer Publisher Info_072621.xlsx"}
        ,{"vendor":"STKA","filename": "data/STKA_CLIENT_ThruADD86.xlsx"}
    ]

cue_sheet = "data/TOO LARGE JENNIFER CUE SHEETS 106 MU.xls"

df = pd.read_excel(cue_sheet, skiprows=15)

print(df.head())
print(len(df))

df.dropna(how="any", inplace=True)

print(len(df))
new_columns = [x.strip() for x in df.columns.tolist()]

df.columns = new_columns
print(df.columns.tolist())


