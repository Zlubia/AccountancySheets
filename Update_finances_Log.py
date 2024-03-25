

class Log :
    def __init__(self, numberoftransactions):
        self.visa = False
        self.skip = []
        self.expenses = []
        self.incomes = []
        self.numberoftransactions = numberoftransactions

    def printlog(self):
        print("------------------------------------------------------")
        print("                         LOGS                         ")
        print("------------------------------------------------------")
        print("\n")

        if self.visa == True :
            print("----------------")
            print("ATTENTION - VISA")
            print("----------------")
            print("")

        print("----------------------EXPENSES-----------------------")
        NumberOfExpenses = len(self.expenses)
        print("\nNumber of encoded expenses is :", NumberOfExpenses)

        print("\nList of expenses :")
        j = 1
        for i in self.expenses:
            print(j, ":", i)
            j += 1

        print("\n----------------------INCOMES-----------------------")
        NumberOfIncomes = len(self.incomes)
        print("\nNumber of encoded incomes is :", NumberOfIncomes)

        print("\nList of incomes :")
        j = 1
        for i in self.incomes:
            print(j, ":", i)
            j +=1

        print("\n--------------SKIPPED TRANSACTIONS-----------------")
        NumberOfSkips = len(self.skip)
        print("\nNumber of skipped transactions is :", NumberOfSkips)

        print("\nList of skipped transactions :")
        j = 1
        for i in self.skip:
            print(j, ":", i)
            j += 1

        if self.numberoftransactions > NumberOfSkips+NumberOfIncomes+NumberOfExpenses :
            print("\n----------------")
            print("   ATTENTION!   ")
            print("----------------")
            print("\nSome transactions have not been treated.")
            print("The amount of transactions received is larger than the amount of transactions treated.")
            print("\nNumber of transactions :", self.numberoftransactions)
            print("Number of Incomes :", NumberOfIncomes)
            print("Number of Expenses :", NumberOfExpenses)
            print("Number of SKIPS :", NumberOfSkips)
        elif self.numberoftransactions < NumberOfSkips+NumberOfIncomes+NumberOfExpenses :
            print("\n----------------")
            print("   ATTENTION!   ")
            print("----------------")
            print("\nSome transactions have been treated twice or more.")
            print("The amount of transactions received is smaller than the amount of transactions treated.")
            print("\nNumber of transactions :", self.numberoftransactions)
            print("Number of Incomes :", NumberOfIncomes)
            print("Number of Expenses :", NumberOfExpenses)
            print("Number of SKIPS :", NumberOfSkips)
        else :
            print("\n-----------------------------------")
            print("\nEvery transaction has been treated.")
            print("\nEnjoy your day !")
