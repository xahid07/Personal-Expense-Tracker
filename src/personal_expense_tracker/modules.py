from datetime import datetime
from collections import defaultdict
from pathlib import Path
import json

#  Always resolve project root dynamically
PROJECT_ROOT = Path(__file__).resolve().parents[2]  
# -> goes up from src/personal_expense_tracker/ to Expense-Tracker/

FILES_DIR = PROJECT_ROOT / "src" / "personal_expense_tracker" / "files"
_file = FILES_DIR / "expense.txt"

# Protected function to Ensure the directory exist...
def _ensure_dir_helper(path: Path) -> Path:
    """
    Ensure a directory exists. If not, create it (with parents).
    Returns the Path object for convenience.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path

_ensure_dir_helper(FILES_DIR)

# Protected function to Create or Update the expense...
def _file_saving_helper(data, file = _file, line_number = None):
    """Protected function: create or update data in a file line by line."""

    # Ensure the directory exists..
    with open(file, "r+" if line_number is not None else "a") as f:

        if line_number is not None:
            lines= f.readlines()
            lines[line_number] = json.dumps(data) + '\n'
            f.seek(0)
            f.writelines(lines)
            f.truncate()
            
        if line_number is None:
            json.dump(data, f)
            f.write('\n')
        print('Data has been updated to the file...')

# Protected Function to Loading Data as dict fomrat...
def _loading_data_helper(file):
    """Protected Function: Return file's in a list of dict format"""
    with open(file, 'r') as f:
        
        try:
            row_data = f.read()
            list_data = row_data.split("\n")
            list_of_dict = [json.loads(line) for line in list_data if line.strip()]
            # json_data = json.dumps(list_of_dict, indent=4)
            return list_of_dict
        except FileNotFoundError:
            return []

# Protected Function to date validation...
def _date_validation_helper(date):
    try:
        valid_date = datetime.strptime(date, "%Y-%m-%d").date()
        return valid_date.strftime("%Y-%m-%d")
    except ValueError:
        return False

def _enumerate_show_helper(data):
    enumerate_data = enumerate(data, start=1)
    for index, expense in enumerate_data:
        print(f"id: {index} ---- Expense Data: {expense}")

def add_expense():
    """Function for adding expense list to the file..."""

    print("All fields are required...")
    
    # Taking User inputs....
    category = input("Enter the expense category (e.g., 'Food', 'Grocery') *: ").strip()
    item = input("Enter the food name *: ").strip()
    expense = (lambda x: float(x) if x.replace(".", "", 1).isdigit() else 0.0)(input("Enter the expense amount *: ").strip() or "0")
    date = input("Enter the expense date (YYYY-MM-DD or 'Today') *: ").strip()

    # Required field validation...
    if not category or not item or not expense or not date:
        print('You did not enter at least one requried field.')
        return
    
    # Validate date format...
    date = _date_validation_helper(date)
    if not date:
        print("Invalid date format. Using today's date instead.")
        date = datetime.today().date().strftime("%Y-%m-%d")
    
    # Making a Dict with all data...
    expense_data = {
        "category": category,
        'item':item,
        "amount": expense,
        "date": date
    }

    # File saving method called...
    _file_saving_helper(expense_data)
    
    print(f"Expense added: {category}, {item}, {expense}, {date}\n")
    
    while True:
        more_input = input("Do you want to add more? (y/n): ").lower().strip()
        if not more_input in ('y', 'yes', 'Yes', 'YES', 'Y'):
            return False
        else:
            add_expense()

def view_expense(file=_file):
    print("All expenses are listed there:");
    list_of_dict = _loading_data_helper(file)
    total_items = len(list_of_dict)
    total_expense = 0
    for data in list_of_dict:
        total_expense += data['amount']
    # json_data = json.dumps(list_of_dict)
    _enumerate_show_helper(list_of_dict)
    print(f"Total items: {total_items} and total expense: ${total_expense:,.2f}")

def update_expense(file = _file):
    """
    Function to update any expense entry based on the user input
    """
    list_of_dict = _loading_data_helper(file)
    count = len(list_of_dict)
    _enumerate_show_helper(list_of_dict)
    choice = input("Select the id to be updated: ").strip()
    if choice.isdigit():
        id = int(choice)
        index = id - 1
        if id in range(1, count+1):
            expense = list_of_dict[index]
            print(f"You have choose: {(id, expense)}")
            print("\n**Update process: blank input for no update...\n")

            category = input("Category: ").strip()
            item = input("Item: ").strip()
            price = (lambda x: float(x) if x or x.replace('.', '', 1).isdigit() else False)(input("Price: ").strip() or False)
            date = input("Date (YYYY-MM-DD): ").strip()
            
            if category:
              expense['category'] = category
            if item:
                expense['item'] = item
            if price:
                expense['amount'] = price
            if date:
                valid_date = _date_validation_helper(date)
                if valid_date:
                    expense['date'] = valid_date
                else:
                    print("Date format incorrect. Kept old date... ")
    
        _file_saving_helper(expense, line_number=index)    

def categorize_expense(file = _file):
    # ---Algorithm
        # 1. Loading existing data in dict format
        # 2. Make another dict of list based on the Similar category.
        # 3. Format: {Food: [{'item':'vagetable', 'amount':221.0,...}, {'item':'vagetable', 'amount':221.0,...}]}
    data = _loading_data_helper(file)
    if data:
        unique_categories = defaultdict(list)
        for entry in data:
            cat = entry['category']
            unique_categories[cat].append(entry)

        for cat, items in unique_categories.items():
            print(f"\nCategory Name: {cat}")
            print('Items on this category:')
            for entry in items:
                print(f"  - {entry['item']} (Amount: {entry['amount']}, Date: {entry['date']})")
            print('\n')
def generate_summary(file = _file):
    list_of_dict = _loading_data_helper(file)
    sorted_list  = sorted(
        list_of_dict,
        key = lambda singleDict: datetime.strptime(singleDict['date'], "%Y-%m-%d")
    )
    _enumerate_show_helper(sorted_list)

    print("Choose which report do you want:\n1.Weekly\n2.Monthly\n3.Yearly\n4.Custom\n")
    choice = input("Enter your choice: ").strip()

    match(choice):
        case '1':
            pass
        case '2':
            pass
        case '3':
            pass
        case '4':
            pass
        case _:
            print('Invalid choice. No summary.')

    