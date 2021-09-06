import Levenshtein as pl
import pandas as pd
import multiprocessing
import math
import time

# print(pl.distance("caser", "case hhh"))

def fuzzy_matcher(test_match, vendors):
    num_processes = int(multiprocessing.cpu_count()/2)
    # calculate the chunk size as an integer
    chunk_size = int(math.ceil(test_match.shape[0]/num_processes))

    # this solution was reworked from the above link.
    # will work even if the length of the dataframe is not evenly divisible by num_processes
    rows = [test_match[i:i + chunk_size] for i in range(0, test_match.shape[0], chunk_size)]

    chunks = [(x, vendors.copy()) for x in rows]
    pool = multiprocessing.Pool(processes=num_processes)

    # # apply our function to each chunk in the list
    result = pool.map(func, chunks)
    
    partial_matches = pd.concat([x[0] for x in result])
    no_matches = pd.concat([x[1] for x in result])
    return partial_matches, no_matches


def match_percent(str1, str2):
    if isinstance(str1, str) and isinstance(str2, str):
        p = 100*(1 - pl.distance(str1, str2)/max([len(str1),len(str2)]))
    else:
        p = 0
    return p

def func(chunk):
    test_match = chunk[0]
    vendors = chunk[1]

    no_match = pd.DataFrame()

    partial_match = pd.DataFrame()

    for index1, row1 in test_match.iterrows():
        found_match = False
        if row1["File Name"].startswith("21S_"):
            no_match = no_match.append(row1)
            continue
        # print("checking "+ str(index1)+" "+ str(row1["File Name"]))
        for index2, row2 in vendors.iterrows():
            
            mp = match_percent(row1["File Name"], row2["File Name"])
            
            if mp > 80:
                found_match = True
                for index, value in row2.items():
                    row1[index] = value
                row1["match_percent"] = mp
                partial_match = partial_match.append(row1)
        
        if found_match:
            continue
        else:
            no_match = no_match.append(row1)

    return (partial_match, no_match)

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
