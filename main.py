import json
import csv
from src.modules import add_expense


if __name__ == "__main__":
    print("\n","*" * 50)
    print(" {:=^50s}".format(" Welcome to the Personal Expense Tracker! "), "\n","*" * 50)
    while True:
        exit = input("Type 'exit' to quit or press Enter to continue: ")
        if(exit.lower().strip() == 'exit'):
            print("Thank you for using the Personal Expense Tracker. Goodbye!")
            break
        choice = input("\n1. Add Expense\n2. View Expenses\n3. Save Expenses\n4. Load Expenses\nPlease choose an option: ")

        if choice == '1':
            # Code to add an expense
            add_expense()
        elif choice == '2':
            # Code to view expenses
            pass
        elif choice == '3':
            # Code to save expenses
            pass
        elif choice == '4':
            # Code to load expenses
            pass
        else:
            print("Invalid choice. Please try again.")