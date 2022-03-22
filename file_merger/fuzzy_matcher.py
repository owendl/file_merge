import Levenshtein as pl
import pandas as pd
import math
import time
from tqdm import tqdm

# print(pl.distance("caser", "case hhh"))

def fuzzy_matcher(test_match, vendors):
    no_match = pd.DataFrame()

    partial_match = pd.DataFrame()

    for index1, row1 in tqdm(test_match.iterrows(), total = test_match.shape[0]):
        found_match = False
        if row1["File Name"].startswith("21S_"):
            no_match = pd.concat([no_match,row1.to_frame().T])
            continue
        # print("checking "+ str(index1)+" "+ str(row1["File Name"]))
        for index2, row2 in vendors.iterrows():
            
            mp = match_percent(row1["File Name"], row2["File Name"])
            
            if mp > 80:
                found_match = True
                for index, value in row2.items():
                    row1[index] = value
                row1["match_percent"] = mp
                partial_match = pd.concat([partial_match,row1.to_frame().T])
        
        if found_match:
            continue
        else:
            no_match = pd.concat([no_match,row1.to_frame().T])
    

    return partial_match, no_match


def match_percent(str1, str2):
    if isinstance(str1, str) and isinstance(str2, str):
        p = 100*(1 - pl.distance(str1, str2)/max([len(str1),len(str2)]))
    else:
        p = 0
    return p


if __name__ == "__main__":
    print("Testing fuzzy matcher")
    
    test_match = pd.read_excel("data/matches.xlsx", sheet_name="No Match")


    vendors = pd.read_excel("data/vendors.xlsx")

    # print(test_match.head())
    # print(vendors.head())
    t1 = time.time()
    partial_matches, no_matches = fuzzy_matcher(test_match, vendors)
    print("finished fuzzy matcher")
    print(math.ceil(time.time()-t1))
    with pd.ExcelWriter("data/matches-test.xlsx") as writer:
        partial_matches.to_excel(writer,sheet_name = "Partial Match",index=False)
        no_matches.to_excel(writer,sheet_name = "Still No Match",index=False)
