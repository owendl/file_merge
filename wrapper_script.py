import file_merger.file_merger as fm

import pandas as pd
import os

print("Starting process")

data = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))

cue_sheet_folder = os.path.join(data, "cue_sheets")
vendor_files_folder = os.path.join(data, "vendor_files")
vendor_file = os.path.join(vendor_files_folder,"vendors.csv")

supported_vendors = ["STKA", "AA", "FTM", "SignatureTracks", "DMS"]

def build_vendor_files():
    if os.path.isfile(vendor_file):
        print("Started reading in consolidated vendor file")
        vendors = pd.read_csv(vendor_file)
        
    else:

        vendor_files = os.listdir(vendor_files_folder)
        print(f"Could not find consolidated vendor file: {vendor_file}, attempting to create one from files in data/vendor_files: {vendor_files}")
        vendors = pd.DataFrame()

        

        for vf in vendor_files:
            print(f"Processing vendor file: {vf}")
            vendor_type = vf.split("_",1)[0]
            # TODO: add a check to see if the vendor file name matches the format options
            if vendor_type not in supported_vendors:
                print(f"Vendor file format {vendor_type} is not one of the currently supported vendor file formats: {supported_vendors}\nSkipping this file")
                continue
            result = getattr(fm, 'format_'+vendor_type)(fm.read_file(vendor_files_folder,vf), final_columns)
            vendors = pd.concat([vendors, result])

        
        vendors.to_csv(vendor_file, index=False)
    print("Vendor information retrieved")
    return vendors



# Modified cue sheet to be read from (modified to remove extra rows before clips portion)

cue_sheets = os.listdir(cue_sheet_folder)

final_columns = ["File Name", "Song Name", "Library", "Composer","Publisher","Catalogue Number"]

def parse_cue_sheet(string, n = 0):
    df = pd.read_excel(string, skiprows = n)
    df.dropna(how="any", inplace=True)
    new_columns = [x.strip() for x in df.columns.tolist()]
    df.columns = new_columns
    df = df.loc[df["CHANNEL"]==1,:]
    df["File Name"]= df["CLIP NAME"].str.split(".",1).str[0]
    return df

vendors = build_vendor_files()

print(f"Working with {len(cue_sheets)} cue sheets ({cue_sheets})")

for cue_sheet in cue_sheets:
    print("Starting with: "+cue_sheet)
    df = parse_cue_sheet(os.path.join(cue_sheet_folder, cue_sheet))

    final = pd.merge(df, vendors, on="File Name", how="left")

    exact_match = final[~final["Library"].isna()]

    no_match = final[final["Library"].isna()]
    print(f"Finished exact match for {cue_sheet}, starting fuzzy match")

    import file_merger.fuzzy_matcher as fuzzy
    partial_match, no_match = fuzzy.fuzzy_matcher(no_match, vendors)

    print(f"Finished fuzzy match for {cue_sheet}, begin writing results")

    with pd.ExcelWriter(os.path.join(data,f"{cue_sheet.split('.')[0]}-matches.xlsx")) as writer:
        exact_match.to_excel(writer,sheet_name = "Exact Match",index=False)
        partial_match.to_excel(writer,sheet_name = "Partial Match",index=False)
        no_match.to_excel(writer,sheet_name = "No Match",index=False)

print("Finished!")