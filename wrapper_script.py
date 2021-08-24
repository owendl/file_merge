import file_merger.file_merger as fm
import pandas as pd



final_columns = ["File Name", "Song Name", "Library", "Composer","Publisher","Catalogue Number"]
# vendor_files = [
#         {"vendor":"FTM","filename": "data/FTM-AA_COMPOSER-PUBLISHER_6-16-21.xlsx", "sheetname":"FTM"}
#         ,{"vendor":"AA","filename": "data/FTM-AA_COMPOSER-PUBLISHER_6-16-21.xlsx", "sheetname":"AA"}
#         ,{"vendor":"SignatureTracks","filename": "data/Signature Tracks - Composer Publisher Info_072621.xlsx"}
#         ,{"vendor":"STKA","filename": "data/STKA_CLIENT_ThruADD86.xlsx"}
#          ,{"vendor":"DMS", "filename": "data/Crazy Legs Productions_Metadata.xlsx", "sheetname":"DMS"}
#     ]
vendor_files=[]
cue_sheet = "data/TOO LARGE JENNIFER CUE SHEETS 106 MU.xls"


def parse_cue_sheet(string):
    df = pd.read_excel(string, skiprows=15)
    df.dropna(how="any", inplace=True)
    new_columns = [x.strip() for x in df.columns.tolist()]
    df.columns = new_columns
    df = df.loc[df["CHANNEL"]==1,:]
    df["File Name"]= df["CLIP NAME"].str.split(".",1).str[0]
    return df

if vendor_files:
    vendors = pd.DataFrame()
    for vf in vendor_files:
        result = getattr(fm, 'format_'+vf.get("vendor"))(fm.read_file(vf), final_columns)
        vendors = pd.concat([vendors, result])

    with pd.ExcelWriter("data/vendors.xlsx") as writer:
        vendors.to_excel(writer, index=False)
else:
    vendors = pd.read_excel("data/vendors.xlsx")

df = parse_cue_sheet(cue_sheet)

final = pd.merge(df, vendors, on="File Name", how="left")

with pd.ExcelWriter("data/matches.xlsx") as writer:
    final[~final["Library"].isna()].to_excel(writer,sheet_name = "Exact Match",index=False)
    final[final["Library"].isna()].to_excel(writer,sheet_name = "No Match",index=False)

