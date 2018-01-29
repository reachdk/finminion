# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 17:24:00 2017

@author: dkumar7
"""

import os
import csv
import pandas as pd

skip_rows = 0
chunk_size = 0
start_check = 'Date'
end_check = 'Total'
cols=['Date', 'Description', 'Withdrawals', 'Deposits', 'Balance']

def readfiles(path):
    append_data = pd.DataFrame([], columns=cols)    
    #directory = os.path.join("c:\\","path")    
    directory = os.path.join(path)
    for root,dirs,files in os.walk(directory):
        for file in files:
           if file.endswith(".csv"):
               filepath = path + '/' +file
               #destpath = path + '/Processed/' + file

               f=open(filepath, 'rt', encoding = 'utf-8' )               

               #  read the transactions part of each file, load, clean and return as append_data
               reader = csv.reader(f, delimiter=',')
               for row in reader:
                   for field in row:
                       if field == start_check:
                           skip_rows = reader.line_num -1
                       if field == end_check:
                           chunk_size = reader.line_num - (skip_rows + 1)
               loaddatatemp = pd.read_csv(filepath, skiprows = skip_rows, chunksize = chunk_size)
               loaddata = pd.concat(loaddatatemp, ignore_index = True)                
               loaddata = loaddata[pd.notnull(loaddata['Date'])]               
               loaddata.rename(columns=lambda x: x.strip(), inplace = True)               
               loaddata['Date'] = pd.to_datetime(loaddata['Date'], dayfirst = True)                
               append_data = append_data.append(loaddata, ignore_index=True)
               f.close()

               #os.rename(filepath, destpath)
    return(append_data)

# call function to read csv files and return data to append
bankdata = readfiles("/Users/dkumar7/Google Drive/finminion/SourceFiles")

# drop columns with all Null values
bankdata = bankdata.dropna(axis = 'columns', how = 'all')
bankdata['Date'] = pd.to_datetime(bankdata['Date'], dayfirst = True)

#load data from master
citimaster = pd.read_csv('/Users/dkumar7/Google Drive/finminion/citi_master.csv')

#strip whitespace from column names
citimaster.rename(columns=lambda x: x.strip(), inplace = True)

#append dataframes
citimaster = citimaster.append(bankdata)

# order columns as desired
citimaster = citimaster[cols]

# write back master
citimaster.to_csv('/Users/dkumar7/Google Drive/finminion/citi_master.csv', index = False)