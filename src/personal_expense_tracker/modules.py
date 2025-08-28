"""
Expense Reporting Module
------------------------

This module provides utilities to manage, store, organize, and generate reports
from personal expense data. Expenses are stored as dictionaries with the
following keys:

    - category (str): Category of the expense (e.g., Food, Travel, Health).
    - item (str): Specific item or purpose of the expense.
    - amount (float): Cost of the expense.
    - date (str): Date of the expense in 'YYYY-MM-DD' format.

Features:
    - Add new expenses interactively.
    - View all expenses in a tabular format with totals.
    - Update existing expenses by ID.
    - Categorize expenses and view them grouped by category.
    - Generate weekly, monthly, or yearly summary reports.
    - Handle month names and numbers interchangeably in monthly reports.
    - Validate dates and ensure required fields are entered.
    - Use Python datetime objects for accurate date manipulation.

Dependencies:
    - datetime (built-in): For parsing and handling dates.
    - collections.defaultdict (built-in): For grouping expenses into reports.
    - pathlib.Path (built-in): For file and directory handling.
    - tabulate (external): For pretty-printing tables.
    - json (built-in): For reading/writing expense data in JSON format.

Usage Examples:
---------------

1. Adding a new expense:
    >>> add_expense()
    Prompts user to input category, item, amount, and date.
    Saves the new expense to the expense file.

2. Viewing all expenses:
    >>> view_expense()
    Prints all saved expenses in a formatted table and shows total count and amount.

3. Updating an existing expense:
    >>> update_expense()
    Prompts user to enter the ID of the expense to update.
    Allows leaving fields blank to retain current values.
    Saves the updated record back to the file.

4. Categorizing expenses:
    >>> categorize_expense()
    Groups all expenses by category and prints each category with its items.

5. Generating summary reports:
    >>> generate_summary()
    Interactively prompts for report type (weekly, monthly, yearly) and period.
    Prints the total items and total expense for the selected period,
    along with detailed entries.

File Storage:
-------------
All expenses are stored in a line-based JSON file located at:
    ./src/personal_expense_tracker/files/expense.txt
Each line represents one expense entry.

Notes:
------
- Dates must be entered in 'YYYY-MM-DD' format; otherwise, today's date will be used.
- Amounts are automatically converted to float; invalid inputs default to 0.0.
- Summary reports handle both month numbers (1-12) and month names (e.g., 'January').
"""


from datetime import datetime
from collections import defaultdict
from pathlib import Path
from tabulate import tabulate
import json


_file = Path("./src/personal_expense_tracker/files/expense.txt")

def _ensure_dir_helper(path: Path) -> Path:
    """
    Ensure that the given directory exists; create it if it does not.

    Args:
        path (Path): Directory path to check or create.

    Returns:
        Path: The original directory path.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path

def _file_saving_helper(data, file=_file, line_number=None):
    """
    Save or update an expense record in a line-based JSON file.

    If `line_number` is provided, the corresponding line in the file is updated.
    Otherwise, the new expense record is appended to the end of the file.

    Args:
        data (dict): Expense entry to save. Must include keys: 'category', 'item', 'amount', 'date'.
        file (Path): File path to store expense data.
        line_number (int, optional): Specific line number to update (1-based index).

    Notes:
        Each expense is stored on a separate line in JSON format.
    """
    _ensure_dir_helper(file.parent)

    if line_number is None:
        # Append mode
        with file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(data) + "\n")
    else:
        # Update mode
        lines = file.read_text(encoding="utf-8").splitlines()
        lines[line_number - 1] = json.dumps(data)
        file.write_text("\n".join(lines), encoding="utf-8")
        print('Data has been updated to the file...')

def _loading_data_helper(file):
    """
    Load expense data from a file and return as a list of dictionaries.

    Args:
        file (Path): Path to the file containing expense records.

    Returns:
        list[dict]: List of expense dictionaries. Returns empty list if file does not exist.
    """
    if not Path(file).exists():
        return []
    with open(file, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]

def _date_validation_helper(date):
    """
    Validate and parse a date string in 'YYYY-MM-DD' format.

    Args:
        date (str): Date string provided by user.

    Returns:
        str | bool: Returns the same date string if valid, otherwise False.
    """
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return date
    except ValueError:
        return False

def _enumerate_show_helper(data):
    """
    Display a list of expense entries in a formatted table with enumeration.

    Args:
        data (list[dict]): List of expense entries. Each entry must have keys:
            'category', 'item', 'amount', 'date'.
    """
    table = [(idx, e['category'], e['item'], e['amount'], e['date']) for idx, e in enumerate(data, 1)]
    print(tabulate(table, headers=["ID", "CATEGORY", "ITEM", "AMOUNT", "DATE"]))

def add_expense():
    """
    Interactively add a new expense entry.

    - Prompts the user to enter category, item, amount, and date.
    - Validates required fields and the date format.
    - Uses today's date if the input date is invalid.
    - Converts the amount to float safely.
    - Saves the expense to the file using `_file_saving_helper`.
    - Recursively allows adding multiple expenses in one session.
    """
    while True:
        print("\nAll fields are required...")
        
        category = input("Enter the expense category (e.g., 'Food', 'Utilities') *: ").strip()
        item = input("Enter the item name *: ").strip()
        amount_input = input("Enter the expense amount *: ").strip() or "0"
        date_input = input("Enter the expense date (YYYY-MM-DD or 'Today') *: ").strip()
        
        if not category or not item:
            print("Category and Item are required. Please try again.")
            continue
        
        amount = float(amount_input) if amount_input.replace(".", "", 1).isdigit() else 0.0
        date = _date_validation_helper(date_input)
        if not date:
            print("Invalid date format. Using today's date instead.")
            date = datetime.today().date().strftime("%Y-%m-%d")
        
        expense_data = {
            "category": category,
            "item": item,
            "amount": amount,
            "date": date
        }
        
        _file_saving_helper(expense_data)
        print(f"Expense added: {category}, {item}, {amount}, {date}\n")
        
        more_input = input("Do you want to add more? (y/n): ").strip().lower()
        if more_input not in ("y", "yes"):
            break

def view_expense(file=_file):
    """
    Display all stored expenses with enumeration and totals.

    - Loads all expenses from the specified file.
    - Prints a formatted table with ID, category, item, amount, and date.
    - Displays the total number of items and the total amount spent.

    Args:
        file (Path, optional): File path containing expense records.
    """
    expenses = _loading_data_helper(file)
    _enumerate_show_helper(expenses)

    total_amount = sum(item["amount"] for item in expenses)
    print(f"\nTotal items: {len(expenses)}")
    print(f"Total expense: {total_amount:,.2f}")

def update_expense(file=_file):
    """
    Update an existing expense entry by its ID.

    - Lists all expenses with IDs.
    - Prompts user for the ID of the expense to update.
    - Allows blank input to retain the original value.
    - Validates the updated date format.
    - Saves the updated entry to the file.

    Args:
        file (Path, optional): File path containing expense records.
    """
    expenses = _loading_data_helper(file)
    _enumerate_show_helper(expenses)
    
    while True:
        try:
            idx = int(input("\nEnter ID to update: "))
            if idx < 1 or idx > len(expenses):
                print("Invalid ID.")
                return
        except ValueError:
            print("Please enter a valid number.")
            return

        expense = expenses[idx - 1]
        print("Leave field blank to keep current value.")

        category = input(f"Enter Category ({expense['category']}): ") or expense['category']
        item = input(f"Enter Item ({expense['item']}): ") or expense['item']
        amount = input(f"Enter Amount ({expense['amount']}): ") or expense['amount']
        date = input(f"Enter Date ({expense['date']}): ") or expense['date']

        updated_expense = {
            "category": category,
            "item": item,
            "amount": float(amount),
            "date": _date_validation_helper(date) or expense['date']
        }
        _file_saving_helper(updated_expense, file, line_number=idx)

        more_input = input("Do you want to update more? (y/n): ").strip().lower()
        if more_input not in ("y", "yes"):
            break

def categorize_expense(file=_file):
    """
    Group and display expenses by category.

    - Loads expenses from the file.
    - Groups entries by 'category'.
    - Prints each category name and lists all items under it with amount and date.

    Args:
        file (Path, optional): File path containing expense records.
    """
    expenses = _loading_data_helper(file)
    categorized = {}
    for e in expenses:
        categorized.setdefault(e["category"], []).append(e)

    for category, items in categorized.items():
        print(f"\nCategory Name: {category}")
        print("Items on this category:")
        for item in items:
            print(f"  - {item['item']} (Amount: {item['amount']}, Date: {item['date']})")

def generate_summary(file=_file):
    """
    Generate and display summary reports: weekly, monthly, or yearly.

    - Loads all expenses from the file.
    - Sorts expenses by date descending.
    - Groups expenses into weekly, monthly, and yearly reports using defaultdict.
    - Provides interactive selection of report type and specific time period.
    - Displays totals and formatted entries per report.

    Args:
        file (Path, optional): File path containing expense records.
    """
    expenses = _loading_data_helper(file)
    expenses.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), reverse=True)

    weekly_report = defaultdict(list)
    monthly_report = defaultdict(list)
    yearly_report = defaultdict(list)

    for e in expenses:
        dt = datetime.strptime(e["date"], "%Y-%m-%d")
        weekly_report[(dt.year, dt.isocalendar().week)].append(e)
        monthly_report[(dt.year, dt.month, dt.strftime('%B'))].append(e)
        yearly_report[dt.year].append(e)

    def _total_return(items):
        """
        Calculate the total number of items and total amount for a list of expenses.

        Args:
            items (list[dict]): List of expense dictionaries.

        Returns:
            tuple: (total_items, total_amount)
        """
        total_amount = sum(x["amount"] for x in items)
        return len(items), total_amount

    def _ordinal(n: int) -> str:
        """
        Convert an integer to its ordinal representation (e.g., 1 -> 1st).

        Args:
            n (int): Number to convert.

        Returns:
            str: Ordinal string.
        """
        if 10 <= n % 100 <= 20:
            return f"{n}th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix}"

    def weeklyReport(year: int, week: int):
        """
        Print a weekly expense report.

        Args:
            year (int): Year of the week.
            week (int): ISO week number (1–52).
        """
        entries = weekly_report[(year, week)]
        if not entries:
            print(f"No expense recorded for week {week} of {year}.")
            return
        total_item, total_amount = _total_return(entries)
        print(f"Weekly report for {_ordinal(week)} week of {year} -> (Total items: {total_item}, Total amount: ${total_amount:,.2f}) :")
        for entry in entries:
            print(f"-- Category: {entry['category']:<15s} | ({entry['item']} for ${entry['amount']:,.2f}) -> {entry['date']}")

    def monthlyReport(year: int, month: int | str):
        """
        Print a monthly expense report.

        Args:
            year (int): Year of the month.
            month (int | str): Month number (1–12) or month name (e.g., 'January').
        """
        keys = monthly_report.keys()
        original_key = tuple()
        for key in keys:
            if set((year, month)).issubset(key):
                original_key = key
                break
        if not original_key:
            print(f"No expense recorded for {month} month of {year}.")
            return
        entries = monthly_report[original_key]
        total_item, total_amount = _total_return(entries)
        print(f"Monthly report for {original_key} -> (Total items: {total_item}, Total amount: ${total_amount:,.2f}) :")
        for entry in entries:
            print(f"-- Category: {entry['category']:<15s} | ({entry['item']} for ${entry['amount']:,.2f}) -> {entry['date']}")

    def yearlyReport(year: int):
        """
        Print a yearly expense report.

        Args:
            year (int): Year to report.
        """
        entries = yearly_report[year]
        if not entries:
            print(f"No expense recorded for year {year}.")
            return
        total_item, total_amount = _total_return(entries)
        print(f"Yearly report for {year} -> (Total items: {total_item}, Total amount: ${total_amount:,.2f}) :")
        for entry in entries:
            print(f"-- Category: {entry['category']:<15s} | ({entry['item']} for ${entry['amount']:,.2f}) -> {entry['date']}")

    print("Choose which report you want:\n1. Weekly\n2. Monthly\n3. Yearly\n")
    choice = input("Enter your choice: ").strip()

    try:
        match(choice):
            case '1':
                year = int(input('Enter the year of the week: ').strip())
                week = int(input('Enter the week number (1 to 52): ').strip())
                weeklyReport(year, week)
            case '2':
                year = int(input('Enter the year: ').strip())
                input_month = input('Enter the month (name/number): ').strip()
                month = int(input_month) if input_month.isdigit() else input_month
                monthlyReport(year, month)
            case '3':
                year = int(input('Enter the year: ').strip())
                yearlyReport(year)
            case _:
                print('Invalid choice. No summary.')
    except Exception as e:
        print(f"Error generating summary: {e}")
