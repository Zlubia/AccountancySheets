# -*- coding: utf-8 -*-
"""
@author: Pierrick
"""
from Update_finances_Log import *
import copy

print("import ezsheets")

import ezsheets

print("import google sheets")

"""
---- Google Sheets to import ---
"""
DataSource = ezsheets.Spreadsheet(
    'https://docs.google.com/spreadsheets/d')

FinanceSpreadsheet = ezsheets.Spreadsheet(
    'https://docs.google.com/spreadsheets/d')

"""
------ VARIABLES ----
"""
ExpensesToWrite = []
IncomeToWrite = []

"""CONSTANTS"""
YES = ["yes", "y", "oui", "o", "ok"]
NO = ["no", "n", "non"]
YESNO = copy.copy(YES)
YESNO.extend(NO)

#building the list of possible categories
CATEGORIES = ['SKIP']
SHEET_Category_Data = FinanceSpreadsheet['Lists et data pour les formules']
for i in range(4, 45): #Expense Categories, numbers are the rows from the sheet
    CATEGORIES.append(SHEET_Category_Data[2, i])
for i in range(4, 11): #Income Categories, numbers are the rows from the sheet
    CATEGORIES.append(SHEET_Category_Data[1,i])

"""
FUNCTIONS
"""


def verify_input(Input, Reference):
    """
    Check if the input received is valid
    Parameters
    ----------
    Input : string - the input received
    Reference : list - the possibles values

    Returns
    -------
    valid : boolean
    """
    if Input in Reference:
        return True
    else:
        print("\nThe input you've given is not valid")
        print("These are possible answers :", Reference)
        return False


def count_filled_rows(Sheet):
    """
    Parameters
    ----------
    Sheet : The Sheet object we're counting rows from

    Returns
    -------
    NumberOfRows : Int
    """
    Data_Column_A = Sheet.getColumn(1)

    NumberOfRows = 0
    for i in Data_Column_A:
        if i == '':
            break
        else:
            NumberOfRows += 1

    return NumberOfRows


def get_month(Date):
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

    MonthIndex = Date[3] + Date[4]
    MonthIndex = int(MonthIndex)

    Month = MonthList[MonthIndex - 1]  # -1 because the index of a list starts at 0
    return Month


def get_amount(Amount):
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
    Amount = Amount.replace(",", ".")
    Amount = float(Amount)
    return Amount


def extract_communication(CommunicationData):
    """
    Parameters
    ----------
    CommunicationData : string containing the communication details from the CSV

    Returns
    -------
    The extracted communication information without the dates and codes and other useless information.
    """
    CutFront = CommunicationData[59:]
    if CutFront.find("BANCONTACT REFERENCE BANQUE") > 0:
        CutEnd = CutFront[:-83]
    elif CutFront.find("VISA DEBIT REFERENCE BANQUE") > 0:
        CutEnd = CutFront[:-83]
    elif CutFront.find("SANS CONTACT REFERENCE BANQUE") > 0:
        CutEnd = CutFront[:-98]
    else :
        CutEnd = CutFront
        print("Error with the details - probably a new type of communication info. Please Check")

    return CutEnd


def get_category_pro_and_detail(TransactionSource):
    """
    TransactionSource : The row of data from the CSV as a list
    DataReferences : dictionary containing the data references
    Returns
    -------
    The Key : Tuple - the key to access the correct value in the DataReferences dictionary
    """

    if TransactionSource[6] == 'Domiciliation':
        Key = (TransactionSource[6], TransactionSource[7], TransactionSource[8])
    elif TransactionSource[6] == 'Paiement par carte':
        Key = (TransactionSource[6], extract_communication(TransactionSource[10]))
    elif TransactionSource[6] == 'Remboursement crédit':
        Key = (TransactionSource[6], TransactionSource[7], TransactionSource[8])
    elif TransactionSource[6] == 'Remboursements Crédits Hypothécaires':
        Key = (TransactionSource[6],)
    elif TransactionSource[6] == 'Ordre permanent':
        Key = (TransactionSource[6], TransactionSource[7], TransactionSource[8], TransactionSource[9].replace("+",""))
    elif TransactionSource[6] == 'Virement en euros' and get_amount(TransactionSource[3]) < 0: #TransactionSource[3] = montant - ceci est une dépense
        Key = (TransactionSource[6], TransactionSource[7], TransactionSource[8], TransactionSource[9].replace("+",""))
    elif TransactionSource[6] == 'Virement instantané en euros' and get_amount(TransactionSource[3]) < 0:  # TransactionSource[3] = montant - ceci est une dépense
        Key = (TransactionSource[6], TransactionSource[7], TransactionSource[8], TransactionSource[9].replace("+", ""))
    elif TransactionSource[6] == 'Virement en euros' and get_amount(TransactionSource[3]) > 0: #TransactionSource[3] = montant - ceci est un revenu
        Key = (TransactionSource[6], TransactionSource[7], TransactionSource[8])
    elif TransactionSource[6] == 'Virement instantané en euros' and get_amount(TransactionSource[3]) > 0: #TransactionSource[3] = montant - ceci est un revenu
        Key = (TransactionSource[6], TransactionSource[7], TransactionSource[8])
    elif TransactionSource[6] == 'Paiement par carte de crédit':
        Key = (TransactionSource[6],)
    elif TransactionSource[6] == 'Frais liés au compte':
        Key = (TransactionSource[6],)

    print("\nhere is the key, beware has to be a tuple !")
    print(Key)

    return Key

"""
------ STEP 01 - Read Data References for the script -------
Create some data structures containing the data references from the finance sheet's reference page (Data For Python Script).
Those data structures will be used later to convert the Data from the CSV to the Data we'll write in the finance sheet.
"""
print("\n------ STEP 01 - Read Data References for the script -------")

SHEET_Data_For_Python_Script = FinanceSpreadsheet['Data For Python Script']

NumberOfRows = count_filled_rows(SHEET_Data_For_Python_Script)

DataReferences = {}
while NumberOfRows > 0:

    CurrentRow = SHEET_Data_For_Python_Script.getRow(NumberOfRows)
    CreateKey = []
    Values = [CurrentRow[0], CurrentRow[1], CurrentRow[2]]
    CurrentRow.pop(2)
    CurrentRow.pop(1)
    CurrentRow.pop(0)

    for j in CurrentRow:
        if j != '':
            CreateKey.append(j)
        else:
            break

    Key = tuple(CreateKey)

    DataReferences[Key] = Values

    NumberOfRows -= 1

print("----")
for i, j in DataReferences.items():
    print(i, j)

"""
------ STEP 02 - Read CSV -------
The transactions are ordered from most recent to oldest ones.
We want to read it from bottom to top, to put the expenses chronologically.
"""

print("\n------ STEP 02 - Read CSV -------")

DataSourceSheet = DataSource[0]  # 0 means the first sheet of the document.
NumberOfRows = count_filled_rows(DataSourceSheet)

Logs = Log(NumberOfRows-1)

print("number of row :")
print(str(NumberOfRows))

while NumberOfRows > 1:

    TransactionSource = DataSourceSheet.getRow(NumberOfRows)
    TransactionToWrite = []

    #Skip les virements vers le compte d'épargne
    Contrepartie = (TransactionSource[7],)
    if DataReferences.get(Contrepartie, 'Empty')[0] == 'Epargne' :
        NumberOfRows -= 1
        Logs.skip.append([TransactionSource[1], "Epargne Automatique"])
        continue

    DateColumn = TransactionSource[1]
    Month = get_month(DateColumn)
    TransactionToWrite.append(Month)

    AccountNumber = (TransactionSource[5],)
    AccountToWrite = DataReferences[AccountNumber][0]

    AmountColumn = TransactionSource[3]
    Amount = get_amount(AmountColumn)

    if Amount < 0:
        EXPENSE = True
        INCOME = False
    else:
        INCOME = True
        EXPENSE = False

    Key = get_category_pro_and_detail(TransactionSource)

    if Key == ('Paiement par carte de crédit',) :
        Logs.visa = True

    Category_Pro_Detail = DataReferences.get(Key, 'DoesNotExist')

    if Category_Pro_Detail == 'DoesNotExist':
        print("\nReference Data Not Found, here is the transaction information :")

        if INCOME == True :
            print("\nATTENTION - This is an income ! ")

        print("\nDate :", TransactionSource[1], ", Amount:", Amount, ", Account: ", AccountToWrite, ", Type:",
              TransactionSource[6])
        print("Contrepartie :", TransactionSource[7], ", Name : ", TransactionSource[8], ", Communication :",
              TransactionSource[9])
        print("Détails: ", extract_communication(TransactionSource[10]))

        InputValidity = False
        while InputValidity == False:
            SkipTransaction = input("\nWould you like to skip this transaction ? Y/N :")
            SkipTransaction.lower()
            InputValidity = verify_input(SkipTransaction, YESNO)
        if SkipTransaction in YES:
            TransactionToWrite.extend([TransactionSource[1], Amount, AccountToWrite, TransactionSource[8], TransactionSource[9], extract_communication(TransactionSource[10])])
            Logs.skip.append(TransactionToWrite)
            NumberOfRows -= 1
            continue

        InputValidity = False
        while InputValidity == False:
            Category = input("\nWich category is attributed to this transaction ? :")
            InputValidity = verify_input(Category, CATEGORIES)

        if EXPENSE == True :
            InputValidity = False
            while InputValidity == False:
                ProExpense = input("\nIs this a professional expense ? Y/N :")
                ProExpense.lower()
                InputValidity = verify_input(ProExpense, YESNO)

            if ProExpense in YES:
                ProExpense = "TRUE"
            else:
                ProExpense = "FALSE"
        else :
            ProExpense = ''

        Comment = input("\nIs there a comment you'd want to add ? :")

        Category_Pro_Detail = [Category, ProExpense, Comment]

        """---Ajout dans les refs---"""
        InputValidity = False
        while InputValidity == False:
            AddToDataReferences = input("\nWould you like to add this information to the reference data ? Y/N :")
            AddToDataReferences.lower()
            InputValidity = verify_input(AddToDataReferences, YESNO)
        if AddToDataReferences in YES:
            #Ajout au dictionnaire des references
            ReferenceToWrite = [Category, ProExpense, Comment]
            DataReferences[Key] = ReferenceToWrite
            #Ecrire dans le google sheet
            ReferenceToWrite.extend(Key)
            LastRow = count_filled_rows(SHEET_Data_For_Python_Script)
            SHEET_Data_For_Python_Script.updateRow(LastRow + 1, ReferenceToWrite)

    TransactionToWrite.extend(Category_Pro_Detail)

    if EXPENSE == True:
        AbsoluteAmount = abs(Amount)
        TransactionToWrite.append(AbsoluteAmount)

        TransactionToWrite.append(AccountToWrite)
        if AccountToWrite == "Commun":
            for i in range(3) :
                TransactionToWrite.append('')
            TransactionToWrite.append(AbsoluteAmount)
            TransactionToWrite[4] = AbsoluteAmount/2

    elif INCOME == True :
        TransactionToWrite.pop(2)
        TransactionToWrite.append(Amount)


    if EXPENSE == True and TransactionToWrite[1] != 'SKIP':
        ExpensesToWrite.append(TransactionToWrite)
        Logs.expenses.append(TransactionToWrite)
    elif INCOME == True and TransactionToWrite[1] != 'SKIP':
        IncomeToWrite.append(TransactionToWrite)
        Logs.incomes.append(TransactionToWrite)
    else :
        Logs.skip.append(TransactionToWrite)

    NumberOfRows -= 1

    print("\nTransaction Data Source : ")
    print(str(TransactionSource))
    print("\nTransaction To Write :")
    print(str(TransactionToWrite))
    print("\nAccount To Write :")
    print(str(AccountToWrite))



"""
------------------ STEP 03 - Write ----------------------------
We write the list of transactions on finance spreadsheet.
"""

"""Writing Expenses"""
ExpenseSheet = FinanceSpreadsheet['Expense']


FilledRows = count_filled_rows(ExpenseSheet)
NextEmptyRow = FilledRows+1

print("List of expenses to write :")
j = 1
for i in ExpensesToWrite :
    #print(j, ":", i)
    ExpenseSheet.updateRow(NextEmptyRow,i)
    NextEmptyRow += 1
    j += 1

"""Writing Income"""
IncomeSheet = FinanceSpreadsheet['Income']

FilledRows = count_filled_rows(IncomeSheet)
NextEmptyRow = FilledRows+1

print("List of incomes to write :")
j = 1
for i in IncomeToWrite :
    #print(j, ":", i)
    IncomeSheet.updateRow(NextEmptyRow,i)
    NextEmptyRow += 1
    j += 1

print("\n Job done !")

Logs.printlog()
