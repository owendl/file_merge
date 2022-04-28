import file_merger.file_merger as fm
import file_merger.multi as fuzzy

import pandas as pd
import os

import math
import multiprocessing
import tqdm


if __name__ == '__main__':
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

        unmatched_rows = len(no_match)
        if unmatched_rows > 0:
            print(f"Finished exact match for {cue_sheet}, starting fuzzy match on {unmatched_rows} unmatched records")

            num_processes = int(multiprocessing.cpu_count()/2)
            # calculate the chunk size as an integer
            chunk_size = int(math.ceil(no_match.shape[0]/(num_processes*5)))

            # will work even if the length of the dataframe is not evenly divisible by num_processes
            rows = [no_match[i:i + chunk_size] for i in range(0, no_match.shape[0], chunk_size)]

            chunks = [(x, vendors.copy()) for x in rows]
            
            with multiprocessing.Pool(processes=num_processes) as p:
                # apply our function to each chunk in the list
                result = list(tqdm.tqdm(p.imap(fuzzy.fuzzy_matcher, chunks), total=len(chunks)))
                
            partial_matches = pd.concat([x[0] for x in result])
            no_matches = pd.concat([x[1] for x in result])
            
            print(f"Finished fuzzy match for {cue_sheet}, begin writing results")

            with pd.ExcelWriter(os.path.join(data,f"{cue_sheet.split('.')[0]}-matches.xlsx")) as writer:
                exact_match.to_excel(writer,sheet_name = "Exact Match",index=False)
                partial_matches.to_excel(writer,sheet_name = "Partial Match",index=False)
                no_matches.to_excel(writer,sheet_name = "No Match",index=False)

        else:
            print(f"Finished exact match for {cue_sheet}, skipping fuzzy match because {len(no_match)} unmatched records and writing results")
            with pd.ExcelWriter(os.path.join(data,f"{cue_sheet.split('.')[0]}-matches.xlsx")) as writer:
                exact_match.to_excel(writer,sheet_name = "Exact Match",index=False)
                

    print("Finished!")