# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 18:17:03 2017

@author: dkumar7
"""

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
start_check = 'Txn Date'
end_check = '**This is a computer generated statement and does not require a signature'
cols=['Txn Date', 'Value Date', 'Description', 'Ref No./Cheque No.', 'Debit', 'Credit', 'Balance']

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
                           skip_rows = reader.line_num - 1
                           print(skip_rows)
                       if field == end_check:
                           chunk_size = reader.line_num - skip_rows - 5
                           print(reader.line_num)
                           print(chunk_size)
               loaddata = pd.read_csv(filepath, skiprows = skip_rows)
               # print(type(loaddatatemp))
               # loaddata = pd.concat(loaddatatemp, ignore_index = True)
               loaddata = loaddata.iloc[:-1,:]
               #loaddata = loaddata[pd.notnull(loaddata['Date'])]               
               loaddata.rename(columns=lambda x: x.strip(), inplace = True)               
               print("test")
               print(loaddata)
               loaddata.to_csv('test.csv')
               loaddata['Txn Date'] = pd.to_datetime(loaddata['Txn Date'], format='%d-%b-%y')                
               print("test1")
               append_data = append_data.append(loaddata, ignore_index=True)
               f.close()

               #os.rename(filepath, destpath)
    return(append_data)

# call function to read csv files and return data to append
bankdata = readfiles("/Users/dkumar7/Google Drive/PyProj/finminion/DKSBISourceFiles")

# drop columns with all Null values
bankdata = bankdata.dropna(axis = 'columns', how = 'all')
bankdata['Txn Date'] = pd.to_datetime(bankdata['Txn Date'], format='%d-%b-%y')

#load data from master
sbimaster = pd.read_csv('/Users/dkumar7/Google Drive/PyProj/finminion/sbi_master.csv')

#strip whitespace from column names
sbimaster.rename(columns=lambda x: x.strip(), inplace = True)

#append dataframes
sbimaster = sbimaster.append(bankdata)

# order columns as desired
sbimaster = sbimaster[cols]

# write back master
sbimaster.to_csv('/Users/dkumar7/Google Drive/PyProj/finminion/sbi_master.csv', index = False)