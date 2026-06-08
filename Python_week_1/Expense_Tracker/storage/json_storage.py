"""
This module handles persistence of expenses and settings using JSON format.
"""

import json
import os
import shutil
from typing import List, Dict, Any

class JSONStorage:

    def __init__(self, expenses_filepath: str = "data/expenses.json", budget_filepath: str = "data/budget.json"):
  
        self.expenses_filepath = expenses_filepath
        self.budget_filepath = budget_filepath
        self._ensure_directories()

    def _ensure_directories(self) -> None:

        for filepath in [self.expenses_filepath, self.budget_filepath]:
            dir_name = os.path.dirname(filepath)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)

    def load_expenses(self) -> List[Dict[str, Any]]:

        if not os.path.exists(self.expenses_filepath):
            return []

        try:
            with open(self.expenses_filepath, "r", encoding="utf-8") as file:
                # If file is empty, return empty list
                content = file.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                if not isinstance(data, list):
                    raise ValueError("Expenses file root element must be a JSON array.")
                return data
        except json.JSONDecodeError as e:
            # Corrupt file case: rename the corrupt file for safety and return empty list
            corrupt_backup = f"{self.expenses_filepath}.corrupt"
            try:
                shutil.copy2(self.expenses_filepath, corrupt_backup)
            except Exception:
                pass
            raise ValueError(
                f"Expenses data file was corrupted. Backed up to {corrupt_backup}. "
                f"Original error: {e}"
            )
        except PermissionError as e:
            raise PermissionError(f"Permission denied accessing expenses file: {e}")

    def save_expenses(self, data: List[Dict[str, Any]]) -> None:

        try:
            self._ensure_directories()
            # Write to a temp file first, then rename (atomic write) to avoid corruption
            temp_filepath = f"{self.expenses_filepath}.tmp"
            with open(temp_filepath, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            os.replace(temp_filepath, self.expenses_filepath)
        except Exception as e:
            raise IOError(f"Failed to write expenses to file: {e}")

    def load_budget(self) -> float:

        if not os.path.exists(self.budget_filepath):
            return 0.0
        try:
            with open(self.budget_filepath, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    return 0.0
                data = json.loads(content)
                return float(data.get("budget", 0.0))
        except (json.JSONDecodeError, KeyError, ValueError, PermissionError):
            return 0.0

    def save_budget(self, amount: float) -> None:

        try:
            self._ensure_directories()
            temp_filepath = f"{self.budget_filepath}.tmp"
            with open(temp_filepath, "w", encoding="utf-8") as file:
                json.dump({"budget": amount}, file, indent=4)
            os.replace(temp_filepath, self.budget_filepath)
        except Exception as e:
            raise IOError(f"Failed to write budget to file: {e}")
