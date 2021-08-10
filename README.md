# file_merge

This repo is a collection of code to help a friend of mine in her work. The problem that she faces is that she needs to collect information related to music tracks used by her company in AV post-production and then upload this data to a website.

So step one is the consolidation of track data from a variety of music track vendors. Each vendor has their own format (column names, formatting, etc.) and this code. To accomodate this I have created a series of custom parsing functions in [file_merger](./file_merger/file_merger). The functions are specific to each vendor (with overlapping code used as needed).

Each function is formatted with the name `format_Vendor()` and has two inputs, a pandas dataframe of the vendor data and a list of strings that are the exepected output columns. Thus far, formatting functions have been built for:
* STKA
* FTMX
* AA
* Signature Tracks
* DMS

