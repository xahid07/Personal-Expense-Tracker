from datetime import datetime
def add_expense():
    print("All fields are required...")
    category = input("Enter the expense category (e.g., 'Food', 'Grocery') *: ").strip()
    food = input("Enter the food name *: ").strip()
    expense = float(input("Enter the expense amount *: ").strip())
    date = input("Enter the expense date (YYYY-MM-DD) *: ").strip()
    # Required field validation
    if not category or not food or not expense or not date:
        print('You did not enter at least one requried field.')
        return
    # Validate date format
    try:
        datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Using today's date instead.")
        date = datetime.now().strftime("%Y-%m-%d")

    expense_data = {
        "category": category,
        "amount": expense,
        "date": datetime.strptime(date, "%Y-%m-%d").date()
    }

    # Here you would typically save the expense to a data structure
    print(f"Expense added: {category}, {expense}, {date}")