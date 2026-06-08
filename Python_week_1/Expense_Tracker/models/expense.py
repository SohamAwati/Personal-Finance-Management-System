"""
This module defines the Expense model representing an individual financial transaction.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class Expense:
 
    expense_id: str
    date: str
    category: str
    description: str
    amount: float

    def to_dict(self) -> Dict[str, Any]:

        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Expense':
   
        try:
            return cls(
                expense_id=str(data["expense_id"]),
                date=str(data["date"]),
                category=str(data["category"]),
                description=str(data["description"]),
                amount=float(data["amount"])
            )
        except (KeyError, ValueError, TypeError) as e:
            raise ValueError(f"Invalid expense data structure: {e}")
