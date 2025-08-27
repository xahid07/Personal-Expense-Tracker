from src.personal_expense_tracker.modules import *


if __name__ == "__main__":
    print("\n","*" * 50)
    print(" {:=^50s}".format(" Welcome to the Personal Expense Tracker! "), "\n","*" * 50)
    
    
    while True:
        exit = input("Type 'exit' to quit or press Enter to continue: ")
        if(exit.lower().strip() == 'exit'):
            print("Thank you for using the Personal Expense Tracker. Goodbye!")
            break
        choice = input("\n1. Add Expense\n2. View Expenses\n3. Update Expenses\n4. Categorize Expenses\n5. Generate Monthly Summery\n6.Export Data\nPlease choose an option: ")

        if choice == '1':
            # Code to add an expense
            add_expense()
        elif choice == '2':
            # Code to view expenses
            view_expense()
        elif choice == '3':
            # Code to update expenses
            update_expense()
        elif choice == '4':
            # Code to categorize expenses
            categorize_expense()
        elif choice == '5':
            # Code to generate monthly summery
            generate_summary()
        elif choice == '6':
            # Code to export reports
            # Export can be choosen from json or csv file format
            pass
        else:
            print("Invalid choice. Please try again.")