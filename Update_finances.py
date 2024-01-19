# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 17:08:14 2024

@author: Pierrick
"""

import ezsheets


"""
---- Google Sheets to import ---
"""
Data_source = ezsheets.Spreadsheet('1KMtkCAud5RhGf9AO7unFJOfK4W3bDJJbZLx3NEJffmA')

Finance_spreadsheet = ezsheets.Spreadsheet('18yFCTPgEwfl9_2pLhC9RMJxkDEX18QyYHozxjmkO_Zc')


"""
------ STEP 01 - Read CSV -------
We want to read it from bottom to top, to put the expenses chronologically.
"""

print("STEP 01")

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
    
    transaction = Data_source_sheet.getRow(number_of_rows)
    number_of_rows -= 1
    
    print(" ")
    print(str(transaction))
    




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
