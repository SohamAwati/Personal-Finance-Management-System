"""
Main entry point for the Personal Finance Management System (PFMS).
Handles user interaction, menu rendering, and links UI with service modules.
"""

from datetime import datetime
import os
import sys
from tabulate import tabulate
from colorama import Fore, Style

from storage.json_storage import JSONStorage
from storage.backup_manager import BackupManager
from services.expense_manager import ExpenseManager
from utils.logger import logger
from utils.validator import (
    ValidationError,
    validate_date,
    validate_category,
    validate_description,
    validate_amount,
    validate_budget
)
from utils.formatter import (
    format_currency,
    print_header,
    print_subheader,
    print_success,
    print_error,
    print_warning,
    format_budget_status
)

def show_menu() -> None:
    print(f"\n{Fore.BLUE}{Style.BRIGHT}===================================================")
    print(f"{Fore.YELLOW}{Style.BRIGHT}         PERSONAL FINANCE MANAGEMENT SYSTEM        ")
    print(f"{Fore.BLUE}{Style.BRIGHT}===================================================")
    print(f"{Fore.GREEN} 1.{Fore.WHITE} Add Expense")
    print(f"{Fore.GREEN} 2.{Fore.WHITE} View Expenses")
    print(f"{Fore.GREEN} 3.{Fore.WHITE} Search Expense")
    print(f"{Fore.GREEN} 4.{Fore.WHITE} Delete Expense")
    print(f"{Fore.GREEN} 5.{Fore.WHITE} Sort Expenses")
    print(f"{Fore.GREEN} 6.{Fore.WHITE} Finance Dashboard")
    print(f"{Fore.GREEN} 7.{Fore.WHITE} Export Report")
    print(f"{Fore.GREEN} 8.{Fore.WHITE} Budget Monitor")
    print(f"{Fore.GREEN} 9.{Fore.WHITE} Exit")
    print(f"{Fore.BLUE}{Style.BRIGHT}===================================================")

def add_expense_flow(manager: ExpenseManager) -> None:
    print_subheader("Add New Expense")
    
    # 1. Date
    default_date = datetime.now().strftime("%Y-%m-%d")
    date_input = input(f"Date (YYYY-MM-DD) [Press Enter for Today: {default_date}]: ").strip()
    if not date_input:
        date_input = default_date
        
    try:
        validated_date = validate_date(date_input)
    except ValidationError as e:
        print_error(str(e))
        logger.warning(f"Invalid Input Attempt - Add Expense Date: '{date_input}'. Error: {e}")
        return

    # 2. Category
    category_input = input("Category (e.g. Food, Travel, Shopping): ").strip()
    try:
        validated_category = validate_category(category_input)
    except ValidationError as e:
        print_error(str(e))
        logger.warning(f"Invalid Input Attempt - Add Expense Category: '{category_input}'. Error: {e}")
        return

    # 3. Description
    description_input = input("Description: ").strip()
    try:
        validated_description = validate_description(description_input)
    except ValidationError as e:
        print_error(str(e))
        logger.warning(f"Invalid Input Attempt - Add Expense Description: '{description_input}'. Error: {e}")
        return

    # 4. Amount
    amount_input = input("Amount (₹): ").strip()
    try:
        validated_amount = validate_amount(amount_input)
    except ValidationError as e:
        print_error(str(e))
        logger.warning(f"Invalid Input Attempt - Add Expense Amount: '{amount_input}'. Error: {e}")
        return

    try:
        expense = manager.add_expense(
            date=validated_date,
            category=validated_category,
            description=validated_description,
            amount=validated_amount
        )
        print_success(f"Expense added successfully! Assigned ID: {expense.expense_id}")
    except Exception as e:
        print_error(f"Failed to save expense: {e}")

def view_expenses_flow(manager: ExpenseManager) -> None:
    print_subheader("All Expenses")
    expenses = manager.get_all_expenses()
    if not expenses:
        print_warning("No expenses recorded yet. Select option 1 to add one.")
        return
        
    headers = ["ID", "Date", "Category", "Description", "Amount"]
    table_data = [
        [exp.expense_id, exp.date, exp.category, exp.description, format_currency(exp.amount)]
        for exp in expenses
    ]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

def search_expense_flow(manager: ExpenseManager) -> None:
  
    print_subheader("Search Expenses")
    print("1. Search by Expense ID")
    print("2. Search by Category")
    print("3. Search by Date")
    print("4. Return to Main Menu")
    
    choice = input("Select search criteria (1-4): ").strip()
    if choice == "1":
        search_type = "id"
        prompt = "Enter search Expense ID (e.g. EXP-0001): "
    elif choice == "2":
        search_type = "category"
        prompt = "Enter search Category: "
    elif choice == "3":
        search_type = "date"
        prompt = "Enter search Date (YYYY-MM-DD or part of date, e.g. 2026-06): "
    elif choice == "4":
        return
    else:
        print_error("Invalid selection.")
        logger.warning(f"Invalid Input Attempt - Search Menu Choice: '{choice}'")
        return

    query = input(prompt).strip()
    if not query:
        print_error("Search term cannot be empty.")
        return
        
    results = manager.search_expense(query, search_type)
    if not results:
        print_warning(f"No results matching '{query}' under search type '{search_type}'.")
        return
        
    headers = ["ID", "Date", "Category", "Description", "Amount"]
    table_data = [
        [exp.expense_id, exp.date, exp.category, exp.description, format_currency(exp.amount)]
        for exp in results
    ]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

def delete_expense_flow(manager: ExpenseManager) -> None:
    print_subheader("Delete Expense")
    expense_id = input("Enter Expense ID to delete (e.g. EXP-0001): ").strip()
    if not expense_id:
        print_error("Expense ID is required.")
        return
        
    # Query exact matching item
    matches = manager.search_expense(expense_id, "id")
    exact_match = None
    for exp in matches:
        if exp.expense_id.upper() == expense_id.upper():
            exact_match = exp
            break
            
    if not exact_match:
        print_error(f"No expense found with ID '{expense_id}'.")
        logger.warning(f"Invalid Input Attempt - Delete non-existent ID: '{expense_id}'")
        return
        
    # Render preview before removing
    headers = ["ID", "Date", "Category", "Description", "Amount"]
    table_data = [[
        exact_match.expense_id,
        exact_match.date,
        exact_match.category,
        exact_match.description,
        format_currency(exact_match.amount)
    ]]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
    
    confirm = input(f"\n{Fore.YELLOW}Are you sure you want to delete this expense? (y/n): ").strip().lower()
    if confirm not in ("y", "yes"):
        print_warning("Deletion cancelled.")
        return
        
    try:
        success = manager.delete_expense(exact_match.expense_id)
        if success:
            print_success(f"Expense {exact_match.expense_id} deleted successfully. Safety backup created.")
        else:
            print_error("Failed to delete expense.")
    except Exception as e:
        print_error(f"Error executing deletion: {e}")

def sort_expenses_flow(manager: ExpenseManager) -> None:
    print_subheader("Sort Expenses")
    print("1. Sort by Date")
    print("2. Sort by Amount")
    print("3. Sort by Category")
    
    choice = input("Select field to sort by (1-3): ").strip()
    if choice == "1":
        sort_by = "date"
    elif choice == "2":
        sort_by = "amount"
    elif choice == "3":
        sort_by = "category"
    else:
        print_error("Invalid selection.")
        logger.warning(f"Invalid Input Attempt - Sort Field Choice: '{choice}'")
        return
        
    print("1. Ascending (Oldest/Smallest/A-Z)")
    print("2. Descending (Newest/Largest/Z-A)")
    order_choice = input("Select sorting order (1-2): ").strip()
    if order_choice == "1":
        reverse = False
    elif order_choice == "2":
        reverse = True
    else:
        print_error("Invalid selection.")
        logger.warning(f"Invalid Input Attempt - Sort Order Choice: '{order_choice}'")
        return
        
    sorted_expenses = manager.sort_expenses(sort_by, reverse)
    if not sorted_expenses:
        print_warning("No expenses recorded yet.")
        return
        
    headers = ["ID", "Date", "Category", "Description", "Amount"]
    table_data = [
        [exp.expense_id, exp.date, exp.category, exp.description, format_currency(exp.amount)]
        for exp in sorted_expenses
    ]
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

def dashboard_flow(manager: ExpenseManager) -> None:
    print_subheader("Expense Analytics Dashboard")
    stats = manager.get_statistics()
    
    if stats["total_entries"] == 0:
        print_warning("No expense data available to display statistics.")
        return
        
    dashboard_data = [
        ["Total Expense Entries", stats["total_entries"]],
        ["Total Capital Expended", format_currency(stats["total_expenses"])],
        ["Average Expense Value", format_currency(stats["average_expense"])],
        ["Highest Expense Entry", format_currency(stats["highest_expense"])],
        ["Lowest Expense Entry", format_currency(stats["lowest_expense"])],
        ["Most Expensive Category", stats["most_expensive_category"]]
    ]
    print(tabulate(dashboard_data, headers=["Metric", "Value"], tablefmt="fancy_grid"))
    
    print_subheader("Category-wise Breakdown")
    breakdown_data = [
        [cat, format_currency(amt)]
        for cat, amt in sorted(stats["category_breakdown"].items(), key=lambda x: x[1], reverse=True)
    ]
    print(tabulate(breakdown_data, headers=["Category", "Total Spent"], tablefmt="fancy_grid"))

def export_report_flow(manager: ExpenseManager) -> None:
    print_subheader("Export Financial Summary Report")
    default_path = "reports/expense_report.txt"
    path_input = input(f"Enter file destination path [Press Enter for default: '{default_path}']: ").strip()
    if not path_input:
        path_input = default_path
        
    try:
        manager.export_report(path_input)
        abs_path = os.path.abspath(path_input)
        print_success("Financial Summary Report successfully generated!")
        print(f"File Location: {abs_path}")
    except Exception as e:
        print_error(f"Failed to generate report: {e}")

def budget_monitor_flow(manager: ExpenseManager) -> None:
    print_subheader("Monthly Budget Monitor")
    
    # Render active limits status
    status_info = manager.get_budget_status()
    budget = status_info["budget"]
    spending = status_info["spending"]
    remaining = status_info["remaining"]
    status_str = status_info["status"]
    
    status_table = [
        ["Monthly Budget Limit", format_currency(budget)],
        ["Current Spending (This Month)", format_currency(spending)],
        ["Remaining Budget Capital", format_currency(remaining)],
        ["Financial Health Status", format_budget_status(status_str)]
    ]
    print(tabulate(status_table, headers=["Budget Parameter", "Value"], tablefmt="fancy_grid"))
    
    # Settings modifications
    change = input("\nDo you want to configure a new monthly budget limit? (y/n): ").strip().lower()
    if change in ("y", "yes"):
        budget_input = input("Enter new monthly budget limit (₹): ").strip()
        try:
            validated_val = validate_budget(budget_input)
            manager.set_budget(validated_val)
            print_success(f"Monthly budget updated successfully to {format_currency(validated_val)}!")
        except ValidationError as e:
            print_error(str(e))
            logger.warning(f"Invalid Input Attempt - Set Budget Value: '{budget_input}'. Error: {e}")
        except Exception as e:
            print_error(f"Error persisting budget limits: {e}")

def main() -> None:
    storage = JSONStorage()
    backup_mgr = BackupManager()
    
    try:
        manager = ExpenseManager(storage, backup_mgr)
    except Exception as e:
        print_error(f"Initialization failure: {e}")
        sys.exit(1)
        
    logger.info("Application Started: Personal Finance Management System.")
    print_header("PERSONAL FINANCE MANAGEMENT SYSTEM")
    
    while True:
        try:
            show_menu()
            choice = input("Select an option (1-9): ").strip()
            
            if choice == "1":
                add_expense_flow(manager)
            elif choice == "2":
                view_expenses_flow(manager)
            elif choice == "3":
                search_expense_flow(manager)
            elif choice == "4":
                delete_expense_flow(manager)
            elif choice == "5":
                sort_expenses_flow(manager)
            elif choice == "6":
                dashboard_flow(manager)
            elif choice == "7":
                export_report_flow(manager)
            elif choice == "8":
                budget_monitor_flow(manager)
            elif choice == "9":
                print(f"\n{Fore.GREEN}Thank you for using the Personal Finance Management System. Goodbye!\n")
                logger.info("Application Terminated normally by User request.")
                break
            else:
                print_error("Invalid input. Please choose an option between 1 and 9.")
                logger.warning(f"Invalid Input Attempt - Main Menu Selection: '{choice}'")
                
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{Fore.GREEN}System interrupted by user. Returning to main menu...\n")
        except Exception as e:
            print_error(f"An unexpected system exception occurred: {e}")
            logger.error(f"Unhandled loop error: {e}", exc_info=True)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.GREEN}System interrupted by user terminal escape. Goodbye!\n")
        logger.info("Application Terminated via KeyboardInterrupt.")
        sys.exit(0)
