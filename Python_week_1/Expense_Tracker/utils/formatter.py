"""
This module provides utility functions for formatting console outputs and text.
"""

import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init(autoreset=True)

def format_currency(amount: float) -> str:
    try:
        # Standard financial formatting with 2 decimal places and thousands commas
        return f"₹{amount:,.2f}"
    except (ValueError, TypeError):
        return f"₹{amount}"

def print_header(title: str) -> None:

    width = 60
    border = "=" * width
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{border}")
    print(f"{Fore.WHITE}{Style.BRIGHT}{title.center(width)}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{border}\n")

def print_subheader(title: str) -> None:

    print(f"\n{Fore.BLUE}{Style.BRIGHT}--- {title} ---")

def print_success(message: str) -> None:
  
    print(f"{Fore.GREEN}✔ {message}")

def print_error(message: str) -> None:
  
    print(f"{Fore.RED}✘ {message}")

def print_warning(message: str) -> None:
   
    print(f"{Fore.YELLOW}⚠ {message}")

def format_budget_status(status: str) -> str:

    if status == "SAFE":
        return f"{Fore.GREEN}{Style.BRIGHT}{status}"
    else:
        return f"{Fore.RED}{Style.BRIGHT}{status}"
