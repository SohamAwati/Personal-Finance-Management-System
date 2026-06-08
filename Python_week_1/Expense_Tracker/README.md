# Personal Finance Management System (PFMS) - Expense Tracker

A production-grade, object-oriented console application in Python designed to track and manage personal expenses. This project demonstrates modular software architecture, file persistence, error handling, strict logging, and formatted terminal outputs.

## Project Overview
The Personal Finance Management System (PFMS) helps users log daily transactions, categorize spendings, analyze monthly budgets, view analytical dashboards, and generate summary financial statements. 

## Features
- **Add Expense**: Insert transaction records with date, category, description, and amount. Auto-assigns serial ID tracking (`EXP-0001`, `EXP-0002`, etc.) and supports defaults.
- **View Expenses**: Displays registered transactions in beautiful grid tables using `tabulate`.
- **Search Expenses**: Multi-criteria lookup (by Expense ID, Category, or Date).
- **Delete Expense**: Removes records safely with confirmation prompts. Triggers a database backup copy automatically before writing deletions.
- **Sort Expenses**: Dynamic list sorting by amount, category, or transaction date.
- **Analytics Dashboard**: Aggregates records to show total/average expenses, highest/lowest entries, category-wise breakdowns, and highlights the most expensive category.
- **Monthly Budget Monitor**: Computes current monthly spending totals against user budget limits. Returns a formatted safe/over-budget warning indicator.
- **Report Export**: Writes statistics summaries and category lists to a readable document: `reports/expense_report.txt`.
- **Automatic Backup System**: Saves backup points to `backups/expense_backup_YYYYMMDD_HHMMSS.json` before deletions.
- **Logging System**: Event trace logging tracking startup, additions, deletions, errors, and invalid input attempts inside `logs/app.log`.

## Technologies Used
- **Language**: Python 3.x
- **Third-Party Libraries**:
  - `colorama`: Cross-platform styled text in command line.
  - `tabulate`: Clean console tables.
  - Built-in modules: `json`, `logging`, `datetime`, `shutil`, `dataclasses`.

## Folder Structure
```
expense_tracker/
├── data/
│   ├── expenses.json
│   └── budget.json
├── backups/
│   └── expense_backup_YYYYMMDD_HHMMSS.json
├── logs/
│   └── app.log
├── reports/
│   └── expense_report.txt
├── models/
│   └── expense.py
├── services/
│   └── expense_manager.py
├── storage/
│   ├── json_storage.py
│   └── backup_manager.py
├── utils/
│   ├── formatter.py
│   ├── validator.py
│   └── logger.py
├── screenshots/
├── requirements.txt
├── main.py
└── README.md
```

## Installation Guide
1. Navigate to the project root directory:
   ```cd Python_week_1/Expense_Tracker```
2. Activate your virtual environment if not already activated. For example, from the workspace root:
   ```source ../../.venv/bin/activate```
3. Install dependencies:
   ```pip install -r requirements.txt```

## Usage Instructions
Run the main runner file:
```bash
python main.py
```
Interact using menu option keys (1-9) to execute features.

## Sample Outputs

### Analytics Dashboard
```
+-----------------------------------+------------+
| Metric                            | Value      |
+===================================+============+
| Total Expense Entries             | 3          |
+-----------------------------------+------------+
| Total Capital Expended            | ₹14,700.00 |
+-----------------------------------+------------+
| Average Expense Value             | ₹4,900.00  |
+-----------------------------------+------------+
| Highest Expense Entry             | ₹7,200.00  |
+-----------------------------------+------------+
| Lowest Expense Entry              | ₹3,000.00  |
+-----------------------------------+------------+
| Most Expensive Category           | Travel     |
+-----------------------------------+------------+
```

### Budget Monitoring Status
```
+-------------------------------+------------+
| Budget Parameter              | Value      |
+===============================+============+
| Monthly Budget Limit          | ₹15,000.00 |
+-------------------------------+------------+
| Current Spending (This Month) | ₹14,700.00 |
+-------------------------------+------------+
| Remaining Budget Capital      | ₹300.00    |
+-------------------------------+------------+
| Financial Health Status       | SAFE       |
+-------------------------------+------------+
```

## Future Enhancements
- Multi-currency support.
- Graphical spending charts (e.g. using matplotlib/plotly).
- Automatic recurring expense scheduling.

## Author Information
- **Developer**: WeIntern Python Software Engineer Intern
- **Role**: Software Development Intern
