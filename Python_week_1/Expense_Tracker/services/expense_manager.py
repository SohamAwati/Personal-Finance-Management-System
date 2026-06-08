"""
This module implements the core business logic of the Personal Finance Management System.
"""

from datetime import datetime
import os
from typing import List, Dict, Any, Optional

from models.expense import Expense
from storage.json_storage import JSONStorage
from storage.backup_manager import BackupManager
from utils.logger import logger


class ExpenseManager:

    def __init__(self, storage: JSONStorage, backup_manager: BackupManager):

        self.storage = storage
        self.backup_manager = backup_manager
        self._expenses: List[Expense] = []
        self._load_expenses_from_storage()

    def _load_expenses_from_storage(self) -> None:
       
        try:
            raw_data = self.storage.load_expenses()
            self._expenses = [Expense.from_dict(d) for d in raw_data]
        except Exception as e:
            logger.error(f"Failed to load expenses on startup: {e}", exc_info=True)
            self._expenses = []
            raise

    def _save_state(self) -> None:
    
        try:
            raw_data = [exp.to_dict() for exp in self._expenses]
            self.storage.save_expenses(raw_data)
        except Exception as e:
            logger.error(f"Failed to save expenses: {e}", exc_info=True)
            raise

    def _generate_next_id(self) -> str:
     
        if not self._expenses:
            return "EXP-0001"
        max_num = 0
        for exp in self._expenses:
            if exp.expense_id.startswith("EXP-"):
                try:
                    num = int(exp.expense_id.split("-")[1])
                    if num > max_num:
                        max_num = num
                except (ValueError, IndexError):
                    pass
        return f"EXP-{max_num + 1:04d}"

    def add_expense(self, date: str, category: str, description: str, amount: float) -> Expense:
   
        expense_id = self._generate_next_id()
        expense = Expense(
            expense_id=expense_id,
            date=date,
            category=category,
            description=description,
            amount=amount
        )
        self._expenses.append(expense)
        self._save_state()
        logger.info(f"Expense Added: ID={expense_id}, Date={date}, Category={category}, Amount=₹{amount:.2f}")
        return expense

    def get_all_expenses(self) -> List[Expense]:
       
        return self._expenses

    def search_expense(self, query: str, search_type: str) -> List[Expense]:
      
        query = query.strip().lower()
        results = []
        for exp in self._expenses:
            if search_type == "id" and query in exp.expense_id.lower():
                results.append(exp)
            elif search_type == "category" and query in exp.category.lower():
                results.append(exp)
            elif search_type == "date" and query in exp.date:
                results.append(exp)
        return results

    def delete_expense(self, expense_id: str) -> bool:
        
        expense_id = expense_id.strip().upper()
        target_index = -1
        target_expense: Optional[Expense] = None
        for i, exp in enumerate(self._expenses):
            if exp.expense_id.upper() == expense_id:
                target_index = i
                target_expense = exp
                break
                
        if target_index == -1 or target_expense is None:
            return False

        try:
            # Generate automated backup before modifications
            backup_path = self.backup_manager.create_backup()
            logger.info(f"Backup Created: {backup_path}")
        except Exception as e:
            logger.error(f"Backup creation failed prior to deleting {expense_id}: {e}", exc_info=True)
            # Re-raise to prevent deletion without safety backup
            raise IOError("Deletion aborted. Could not create safety backup file.")

        # Pop from memory list and persist
        self._expenses.pop(target_index)
        self._save_state()
        logger.info(f"Expense Deleted: ID={expense_id}, Details: {target_expense.to_dict()}")
        return True

    def sort_expenses(self, sort_by: str, reverse: bool = False) -> List[Expense]:
       
        if sort_by == "date":
            return sorted(self._expenses, key=lambda x: x.date, reverse=reverse)
        elif sort_by == "amount":
            return sorted(self._expenses, key=lambda x: x.amount, reverse=reverse)
        elif sort_by == "category":
            return sorted(self._expenses, key=lambda x: x.category.lower(), reverse=reverse)
        return list(self._expenses)

    def get_statistics(self) -> Dict[str, Any]:
       
        if not self._expenses:
            return {
                "total_expenses": 0.0,
                "total_entries": 0,
                "average_expense": 0.0,
                "highest_expense": 0.0,
                "lowest_expense": 0.0,
                "most_expensive_category": "N/A",
                "category_breakdown": {}
            }
            
        total_expenses = sum(exp.amount for exp in self._expenses)
        total_entries = len(self._expenses)
        average_expense = total_expenses / total_entries
        
        highest_exp = max(self._expenses, key=lambda x: x.amount)
        lowest_exp = min(self._expenses, key=lambda x: x.amount)
        
        category_breakdown = {}
        for exp in self._expenses:
            # Standardize category text for grouping
            cat = exp.category.title()
            category_breakdown[cat] = category_breakdown.get(cat, 0.0) + exp.amount
            
        most_expensive_cat = max(category_breakdown, key=category_breakdown.get) if category_breakdown else "N/A"
        
        return {
            "total_expenses": total_expenses,
            "total_entries": total_entries,
            "average_expense": average_expense,
            "highest_expense": highest_exp.amount,
            "lowest_expense": lowest_exp.amount,
            "most_expensive_category": most_expensive_cat,
            "category_breakdown": category_breakdown
        }

    def export_report(self, filepath: str = "reports/expense_report.txt") -> str:
       
        stats = self.get_statistics()
        report_dir = os.path.dirname(filepath)
        if report_dir:
            os.makedirs(report_dir, exist_ok=True)

        try:
            with open(filepath, "w", encoding="utf-8") as file:
                file.write("===================================================\n")
                file.write("             PERSONAL FINANCE SUMMARY REPORT        \n")
                file.write("===================================================\n")
                file.write(f"Date Generated    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write(f"Total Entries     : {stats['total_entries']}\n")
                file.write(f"Total Expenses    : ₹{stats['total_expenses']:,.2f}\n")
                file.write(f"Average Expense   : ₹{stats['average_expense']:,.2f}\n")
                file.write(f"Highest Expense   : ₹{stats['highest_expense']:,.2f}\n")
                file.write(f"Lowest Expense    : ₹{stats['lowest_expense']:,.2f}\n")
                file.write(f"Most Costly Cat   : {stats['most_expensive_category']}\n")
                file.write("---------------------------------------------------\n")
                file.write("              CATEGORY BREAKDOWN                   \n")
                file.write("---------------------------------------------------\n")
                for cat, amt in sorted(stats["category_breakdown"].items(), key=lambda x: x[1], reverse=True):
                    file.write(f"{cat:<18} : ₹{amt:,.2f}\n")
                file.write("===================================================\n")
                
            logger.info(f"Report Generated: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to export report: {e}", exc_info=True)
            raise IOError(f"Could not export report file: {e}")

    # --- Budget Management ---

    def set_budget(self, amount: float) -> None:
       
        try:
            self.storage.save_budget(amount)
            logger.info(f"Budget Configured: ₹{amount:.2f}")
        except Exception as e:
            logger.error(f"Failed to set budget: {e}", exc_info=True)
            raise

    def get_budget(self) -> float:
        """Loads configured monthly budget."""
        return self.storage.load_budget()

    def get_budget_status(self) -> Dict[str, Any]:
    
        current_month = datetime.now().strftime("%Y-%m")
        monthly_expenses = [
            exp.amount for exp in self._expenses if exp.date.startswith(current_month)
        ]
        current_spending = sum(monthly_expenses)
        budget = self.get_budget()
        remaining = budget - current_spending
        status = "SAFE" if current_spending <= budget else "OVER BUDGET"
        
        return {
            "budget": budget,
            "spending": current_spending,
            "remaining": remaining,
            "status": status
        }
