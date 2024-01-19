# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 17:08:14 2024

@author: Pierrick
"""

import ezsheets


#ss = ezsheets.upload('CSV_2024-01-17-16.24.csv')

test_spreadsheet = ezsheets.Spreadsheet('18yFCTPgEwfl9_2pLhC9RMJxkDEX18QyYHozxjmkO_Zc')

#Getting first sheet :
Expense_sheet = test_spreadsheet['Expense']

"""
loop = True
i = 1

while loop == True :
    
    if Expense_sheet[1,i] == '' :
        loop = False
        Expense_sheet[1,i] = 'OCT'
        
    else :
        i += 1
"""

column_A = Expense_sheet.getColumn(1)

j = 0

for i in column_A:
    j += 1
    
    if i == '' :
        Expense_sheet[1,j] = 'OCT'
        break