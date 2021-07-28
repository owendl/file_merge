import os
import pandas as pd
import argparse


def generic():
    print("generic function")

def read_vendor_file(input):
    sheetname= input.get("sheetname", 0)
    df = pd.read_excel(input.get("filename"), sheet_name=sheetname)
    df["Library"] = input.get("vendor")
    return df

def format_STKA(df):
    '''
    function for custom processing of STKA formatted vendor excel file

    input: pandas DataFrame with the following columns: ["Track Title", "Composer","Publisher","Duration"]

    output: pandas DataFrame with columns specified by final_columns
        ex. ["File Name", "Song Name", "Library", "Composer","Publisher","Catalogue Number"]
    '''

    df["Song Name"]=df["Track Title"].str[len("STKA_"):]
    df.rename(columns = {"Track Title":"File Name"}, inplace=True)
    df["Catalogue Number"] = ""
    return df[final_columns]

def format_AA(df):
    '''
        function for custom processing of FTM formatted vendor excel file

        input: pandas DataFrame with the following columns: ["Cue Title", "Writers", "Publishers", "ISRC"]

        output: pandas DataFrame with columns specified by final_columns
            ex. ["File Name", "Song Name", "Library", "Composer","Publisher","Catalogue Number"]
    '''
    df.rename(columns = {"Cue Title":"File Name", "Writers":"Composer", "Publishers":"Publisher", "ISRC":"Catalogue Number"}, inplace=True)
    df["Song Name"]=df["File Name"].str[len("AA_"):]
    return df[final_columns]

def format_FTM(df):
    '''
        function for custom processing of FTM formatted vendor excel file

        input: pandas DataFrame with the following columns: ["Cue Title", "Writers", "Publishers", "ISRC"]

        output: pandas DataFrame with columns specified by final_columns
            ex. ["File Name", "Song Name", "Library", "Composer","Publisher","Catalogue Number"]
    '''    
    df.rename(columns = {"Cue Title":"File Name", "Writers":"Composer", "Publishers":"Publisher", "ISRC":"Catalogue Number"}, inplace=True)
    df["Song Name"]=df["File Name"].str[len("FTMX_"):]

    return df[final_columns]

def format_SignatureTracks(df):
    '''
    TODO
    function for custom processing of Signature Tracks formatted vendor excel file

    input: pandas DataFrame with the following columns: [Title	Publisher 1 Company	Publisher 1 Pro Affiliation	Publisher 1 CAE/IPI	Publisher 1 Ownership Share	Publisher 1 Role	Publisher 1 Collection Share Percentage 1	Publisher 1 Collection Share Territory 1	Publisher 2 Company	Publisher 2 Pro Affiliation	Publisher 2 CAE/IPI	Publisher 2 Ownership Share	Publisher 2 Role	Publisher 2 Collection Share Percentage 1	Publisher 2 Collection Share Territory 1	Publisher 3 Company	Publisher 3 Pro Affiliation	Publisher 3 CAE/IPI	Publisher 3 Ownership Share	Publisher 3 Role	Publisher 3 Collection Share Percentage 1	Publisher 3 Collection Share Territory 1	Publisher 4 Company	Publisher 4 Pro Affiliation	Publisher 4 CAE/IPI	Publisher 4 Ownership Share	Publisher 4 Role	Publisher 4 Collection Share Percentage 1	Publisher 4 Collection Share Territory 1	Publisher 5 Company	Publisher 5 Pro Affiliation	Publisher 5 CAE/IPI	Publisher 5 Ownership Share	Publisher 5 Role	Publisher 5 Collection Share Percentage 1	Publisher 5 Collection Share Territory 1	Writer 1 First Name	Writer 1 Last Name	Writer 1 Company	Writer 1 Pro Affiliation	Writer 1 CAE/IPI	Writer 1 Ownership Share	Writer 1 Publishing Interest	Writer 1 Role	Writer 2 First Name	Writer 2 Last Name	Writer 2 Company	Writer 2 Pro Affiliation	Writer 2 CAE/IPI	Writer 2 Ownership Share	Writer 2 Publishing Interest	Writer 2 Role	Writer 3 First Name	Writer 3 Last Name	Writer 3 Company	Writer 3 Pro Affiliation	Writer 3 CAE/IPI	Writer 3 Ownership Share	Writer 3 Publishing Interest	Writer 3 Role	Writer 4 First Name	Writer 4 Last Name	Writer 4 Company	Writer 4 Pro Affiliation	Writer 4 CAE/IPI	Writer 4 Ownership Share	Writer 4 Publishing Interest	Writer 4 Role	Writer 5 First Name	Writer 5 Last Name	Writer 5 Company	Writer 5 Pro Affiliation	Writer 5 CAE/IPI	Writer 5 Ownership Share	Writer 5 Publishing Interest	Writer 5 Role	Writer 6 First Name	Writer 6 Last Name	Writer 6 Company	Writer 6 Pro Affiliation	Writer 6 CAE/IPI	Writer 6 Ownership Share	Writer 6 Publishing Interest	Writer 6 Role	Writer 7 First Name	Writer 7 Last Name	Writer 7 Company	Writer 7 Pro Affiliation	Writer 7 CAE/IPI	Writer 7 Ownership Share	Writer 7 Publishing Interest	Writer 7 Role]

    output: pandas DataFrame with columns specified by final_columns
        ex. ["File Name", "Song Name", "Library", "Composer","Publisher","Catalogue Number"]
    
    '''
    return df

if __name__ == "__main__":
    print("Running file merger")
    final_columns = ["File Name", "Song Name", "Library", "Composer","Publisher","Catalogue Number"]
    vendor_files = [
        {"vendor":"FTM","filename": "data/FTM-AA_COMPOSER-PUBLISHER_6-16-21.xlsx", "sheetname":"FTM"}
        ,{"vendor":"AA","filename": "data/FTM-AA_COMPOSER-PUBLISHER_6-16-21.xlsx", "sheetname":"AA"}
        ,{"vendor":"SignatureTracks","filename": "data/Signature Tracks - Composer Publisher Info_072621.xlsx"}
        ,{"vendor":"STKA","filename": "data/STKA_CLIENT_ThruADD86.xlsx"}
    ]

    df = format_AA(read_vendor_file(vendor_files[1]))
    print(df.head())
    