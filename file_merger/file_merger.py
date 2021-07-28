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
    TODO
    '''
    return df

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

    df = format_FTM(read_vendor_file(vendor_files[0]))
    print(df.head())
    