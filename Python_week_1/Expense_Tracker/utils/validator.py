"""
This module provides functions for validating user input data for expenses.
"""

from datetime import datetime

class ValidationError(ValueError):
    pass

def validate_date(date_str: str) -> str:

    date_str = date_str.strip()
    try:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValidationError("Date must be in YYYY-MM-DD format and represent a valid calendar date.")

    if parsed_date.date() > datetime.now().date():
        raise ValidationError("Expense date cannot be in the future.")

    return date_str

def validate_category(category_str: str) -> str:

    category_str = category_str.strip()
    if not category_str:
        raise ValidationError("Category name cannot be empty.")
    if len(category_str) > 30:
        raise ValidationError("Category name must be 30 characters or less.")
    # Title case for consistency
    return category_str.title()

def validate_description(description_str: str) -> str:
  
    description_str = description_str.strip()
    if not description_str:
        raise ValidationError("Description cannot be empty.")
    if len(description_str) > 100:
        raise ValidationError("Description must be 100 characters or less.")
    return description_str

def validate_amount(amount_str: str) -> float:

    try:
        # Replace common symbol if typed by mistake
        clean_amount = amount_str.replace("₹", "").replace(",", "").strip()
        amount = float(clean_amount)
    except ValueError:
        raise ValidationError("Amount must be a numeric value.")
        
    if amount <= 0:
        raise ValidationError("Amount must be a positive number greater than zero.")
        
    return amount

def validate_budget(budget_str: str) -> float:
 
    try:
        clean_budget = budget_str.replace("₹", "").replace(",", "").strip()
        budget = float(clean_budget)
    except ValueError:
        raise ValidationError("Budget must be a numeric value.")
        
    if budget < 0:
        raise ValidationError("Budget cannot be negative.")
        
    return budget
