import file_merger.file_merger as fm

import pandas as pd

# Flag whether to run the building of the vendor file
# If run_vendors = True, then all of the specified vendor files will be read incrementally, consolidated and written to a new file
# If run_vendors = False, then it will skip the reading and consolidating and try to read from a previously written vendors file
run_vendors = True

# Modified cue sheet to be read from (modified to remove extra rows before clips portion)
cue_sheet = "data/TLC-1KBFF-101 ITE MUSIC CUES.xlsx"

# Most recent vendor database files 
vendor_files = [
        {"vendor":"FTM","filename": "data/FTM-AA_COMPOSER-PUBLISHER_6-16-21.xlsx", "sheetname":"FTM"},
        {"vendor":"AA","filename": "data/FTM-AA_COMPOSER-PUBLISHER_6-16-21.xlsx", "sheetname":"AA"},
        {"vendor":"SignatureTracks","filename": "data/Signature Tracks - Composer Publisher Info_072621.xlsx"},
        {"vendor":"STKA","filename": "data/STKA_CLIENT_ThruADD86.xlsx"},
          {"vendor":"DMS", "filename": "data/DMS_FullCatalog_2022-01-11.xlsx"},
    ]


final_columns = ["File Name", "Song Name", "Library", "Composer","Publisher","Catalogue Number"]

def parse_cue_sheet(string, n = 0):
    df = pd.read_excel(string, skiprows = n)
    df.dropna(how="any", inplace=True)
    new_columns = [x.strip() for x in df.columns.tolist()]
    df.columns = new_columns
    df = df.loc[df["CHANNEL"]==1,:]
    df["File Name"]= df["CLIP NAME"].str.split(".",1).str[0]
    return df

if run_vendors:
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

exact_match = final[~final["Library"].isna()]

no_match = final[final["Library"].isna()]


import file_merger.fuzzy_matcher as fuzzy
partial_match, no_match = fuzzy.fuzzy_matcher(no_match, vendors)

with pd.ExcelWriter(f"data/{cue_sheet.split('.')[0][5:]}-matches.xlsx") as writer:
    exact_match.to_excel(writer,sheet_name = "Exact Match",index=False)
    partial_match.to_excel(writer,sheet_name = "Partial Match",index=False)
    no_match.to_excel(writer,sheet_name = "No Match",index=False)

