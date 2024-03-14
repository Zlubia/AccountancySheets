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
DataSource = ezsheets.Spreadsheet('https://docs.google.com/spreadsheets/')

FinanceSpreadsheet = ezsheets.Spreadsheet('https://docs.google.com/spreadsheets/')

"""
------ VARIABLES ----
"""
ExpensesToWrite = []

"""
FUNCTIONS
"""

def get_month(Date) :
    """
    Parameters
    ----------
    date : string
        Date is written in this format : 14/01/2024

    Returns
    -------
    The first 3 letters of the month. For example 'JAN'
    """
    MonthList = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    
    MonthIndex = Date[3]+Date[4]
    MonthIndex = int(MonthIndex)
    
    Month = MonthList[MonthIndex-1]  #-1 because the index of a list starts at 0
    return Month

def get_amount(Amount) :
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
    Amount = Amount.replace(",",".")
    Amount = float(Amount)
    return Amount

def extract_communication(CommunicationData) :
    """
    Parameters
    ----------
    CommunicationData : string containing the communication details from the CSV

    Returns
    -------
    The extracted communication information without the dates and codes and other useless information.
    """
    CutFront = CommunicationData[59:]
    CutEnd = CutFront[:-83]

    return CutEnd

def get_category_pro_and_detail(TransactionSource, DataReferences):
    """
    TransactionSource : The row of data from the CSV as a list
    DataReferences : dictionary containing the data references
    Returns
    -------
    A string of the category of the transaction
    """

    if TransactionSource[6] == 'Domiciliation':
        Key = (TransactionSource[6], TransactionSource[7], TransactionSource[8])
    elif TransactionSource[6] == 'Paiement par carte':
        Key = (TransactionSource[6], extract_communication(TransactionSource[10]))
    elif TransactionSource[6] == 'Remboursements Crédits Hypothécaires':
        Key = (TransactionSource[6],)
    elif TransactionSource[6] == 'Ordre permanent':
        Key = (TransactionSource[6], TransactionSource[7], TransactionSource[8],TransactionSource[9])
    elif TransactionSource[6] == 'Virement en euros':
        Key = (TransactionSource[6], TransactionSource[7], TransactionSource[8],TransactionSource[9])

    print("here is the key, beware has to be a tuple !")
    print(Key)
    Values = DataReferences.get(Key, 'DoesNotExist')

    return Values


"""
------ STEP 01 - Read Data References for the script -------
Create some data structures containing the data references from the finance sheet's reference page (Data For Python Script).
Those data structures will be used later to convert the Data from the CSV to the Data we'll write in the finance sheet.
"""
print("\n------ STEP 01 - Read Data References for the script -------")



SHEET_Data_For_Python_Script = FinanceSpreadsheet['Data For Python Script']
Data_Column_A = SHEET_Data_For_Python_Script.getColumn(1)



"""Create a function for counting rows?"""
NumberOfRows = 0
for i in Data_Column_A :
    if i == '' :
        break
    else :
        NumberOfRows += 1
        

        

DataReferences = {}
while NumberOfRows > 0 :
    
    CurrentRow = SHEET_Data_For_Python_Script.getRow(NumberOfRows)
    CreateKey = []
    Values = [CurrentRow[0],CurrentRow[1],CurrentRow[2]]
    CurrentRow.pop(2)
    CurrentRow.pop(1)
    CurrentRow.pop(0)
    
    for j in CurrentRow :
        if j != '':
            CreateKey.append(j)
        else :
            break

    Key = tuple(CreateKey)

    DataReferences[Key] = Values
    
    NumberOfRows -= 1
    
print("----")
for i,j in DataReferences.items():
    print(i, j)



"""
------ STEP 02 - Read CSV -------
The transactions are ordered from most recent to oldest ones.
We want to read it from bottom to top, to put the expenses chronologically.
"""

print("\n------ STEP 02 - Read CSV -------")

DataSourceSheet = DataSource[0]  # 0 means the first sheet of the document.

Data_Column_A = DataSourceSheet.getColumn(1)
NumberOfRows = 0

for i in Data_Column_A :
    if i == '' :
        break
    else :
        NumberOfRows += 1
        

    
print("number of row :")
print(str(NumberOfRows))

while NumberOfRows > 1 :
    
    TransactionSource = DataSourceSheet.getRow(NumberOfRows)
    TransactionToWrite = []
    
    DateColumn = TransactionSource[1]
    Month = get_month(DateColumn)
    TransactionToWrite.append(Month)

    AmountColumn = TransactionSource[3]
    Amount = get_amount(AmountColumn)
    
    if Amount < 0 :
        EXPENSE = True
        INCOME = False
    else :
        INCOME = True
        EXPENSE = False

    Category_Pro_Detail = get_category_pro_and_detail(TransactionSource,DataReferences)
    if Category_Pro_Detail != 'DoesNotExist':
        TransactionToWrite.extend(Category_Pro_Detail)
    #else :
        #Faudra ajouter ici l'option de demander un input et d'écrire un nouveau truc dans les data etc.

    if EXPENSE == True :
        AbsoluteAmount = abs(Amount)
        TransactionToWrite.append(AbsoluteAmount)

    AccountNumber = (TransactionSource[5],)
    AccountToWrite = DataReferences[AccountNumber][0]
    TransactionToWrite.append(AccountToWrite)

    if EXPENSE == True:
        ExpensesToWrite.append(TransactionToWrite)
    
    NumberOfRows -= 1
    
    print("\nTransaction Data Source : ")
    print(str(TransactionSource))
    print("\nTransaction To Write :")
    print(str(TransactionToWrite))
    print("\nAccount To Write :")
    print(str(AccountToWrite))
    
print("List of expenses to write")
print(ExpensesToWrite)


ExpenseSheet = FinanceSpreadsheet['Expense']


"""Cette version-ci permet de faire une loop sans devoir se connecter au google sheet à chaque vérification de la boucle.
On memorise la colonne entière, et je parcours la colonne.
"""
column_A = ExpenseSheet.getColumn(1)

j = 0

for i in column_A:
    j += 1
    
    if i == '' :
        ExpenseSheet[1,j] = 'OCT'
        break


    
print ("\n testing done")
    
"""
----------
OK Je peux utiliser des inputs pour donner des indications !
----------
"""
  
b = input("trying an imput here")

#Expense_sheet[11,11] = b
