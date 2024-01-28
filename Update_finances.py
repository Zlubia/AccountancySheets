# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 17:08:14 2024

@author: Pierrick
"""

print("import ezsheets")

import ezsheets

print("import google sheets")

"""
---- Google Sheets to import ---
"""
Data_source = ezsheets.Spreadsheet('https://docs.google.com/spreadsheets/d/1KMtkCAud5RhGf9AO7unFJOfK4W3bDJJbZLx3NEJffmA/edit#gid=1309867271')

Finance_spreadsheet = ezsheets.Spreadsheet('https://docs.google.com/spreadsheets/d/18yFCTPgEwfl9_2pLhC9RMJxkDEX18QyYHozxjmkO_Zc/edit#gid=436550579')

"""
FUNCTIONS
"""

def getmonth(date) :
    """
    Parameters
    ----------
    date : string
        Date is written in this format : 14/01/2024

    Returns
    -------
    The first 3 letters of the month. For example 'JAN'
    """
    monthlist = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    
    month_index = date[3]+date[4]
    month_index = int(month_index)
    
    month = monthlist[month_index-1]  #-1 because the index of a list starts at 0
    return month

def getamount(amount) :
    """
    Converts the written(string) amount to a float
    Parameters
    ----------
    amount : string
        Amount is the 4th column of data. It's written as a string with a comma instead of a point.

    Returns
    -------
    The amount converted to float
    """
    amount = amount.replace(",",".")
    amount = float(amount)
    return amount


"""
------ STEP 01 - Read CSV -------
The transactions are ordered from most recent to oldest ones.
We want to read it from bottom to top, to put the expenses chronologically.
"""

print("\nSTEP 01")

Data_source_sheet = Data_source[0]  # 0 means the first sheet of the document.

Data_column_A = Data_source_sheet.getColumn(1)
number_of_rows = 0

for i in Data_column_A :
    if i == '' :
        break
    else :
        number_of_rows += 1
    
print("number of row :")
print(str(number_of_rows))

while number_of_rows > 1 :
    
    transaction_source = Data_source_sheet.getRow(number_of_rows)
    transaction_to_write = []
    
    date_column = transaction_source[1]
    month = getmonth(date_column)    
    transaction_to_write.append(month)
    
    
    amount_column = transaction_source[3]
    amount = getamount(amount_column)
    
    if amount < 0 :
        EXPENSE = True
        INCOME = False
    else :
        INCOME = True
        EXPENSE = False
    
    number_of_rows -= 1
    
    print("\nTransaction Data Source : ")
    print(str(transaction_source))
    print("\nTransaction To Write :")
    print(str(transaction_to_write))
    




Expense_sheet = Finance_spreadsheet['Expense']


"""Cette version-ci permet de faire une loop sans devoir se connecter au google sheet à chaque vérification de la boucle.
On memorise la colonne entière, et je parcours la colonne.
"""
column_A = Expense_sheet.getColumn(1)

j = 0

for i in column_A:
    j += 1
    
    if i == '' :
        Expense_sheet[1,j] = 'OCT'
        break
    
    
print ("/n testing done")
    
"""
----------
OK Je peux utiliser des inputs pour donner des indications !
----------
"""
  
b = input("trying an imput here")

#Expense_sheet[11,11] = b
