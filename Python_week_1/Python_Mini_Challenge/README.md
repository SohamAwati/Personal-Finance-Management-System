# Python Problem Solving Toolkit

A comprehensive, production-ready Python command-line utility toolkit designed to solve common algorithmic challenges in string manipulation, list operations, and dictionary handling. Built with professional engineering practices, full type hinting, automated test coverage, session-based telemetry, logging, and automatic reporting.

## Project Overview

This toolkit provides modular, highly optimized, and robust solutions to 21 classic coding challenges, structured to act like a real-world developer's utility library rather than a simple script dump. The toolkit features:
* **Robust Error Handling**: Input validation and custom exception raising for edge cases.
* **Telemetry & Dashboard**: Session statistics tracking active category runs, execution times, and counts.
* **Logging System**: Automatic event, action, and error logging to a local file.
* **Report Exporter**: Generates structured reports showing inputs, outputs, timestamps, and execution status.
* **Interactive CLI System**: Menus for individual function testing with custom or default inputs.

---

## Folder Structure

```
Python_Mini_Challenge/
├── string_challenges.py        # String manipulation algorithms
├── list_challenges.py          # List search, processing, and sorting algorithms
├── dictionary_challenges.py    # Dictionary transformations and deep search utilities
├── main.py                     # CLI Interactive Menu, dashboard, logger, and exporter
├── test_challenges.py          # Comprehensive Pytest & Unittest test suite
├── README.md                   # Project documentation
├── logs/
│   └── app.log                 # Persistent runtime log file
├── reports/
│   └── challenge_report.txt    # Session execution summaries and outputs
└── screenshots/                # Application demonstration captures
```

---

## Features

### 1. Challenge Suites

#### String Challenges (`string_challenges.py`)
1. **Reverse a String**: Inverts character order using slicing.
2. **Count Vowels**: Case-insensitive matching and counting.
3. **Palindrome Check**: Verifies palindromes ignoring non-alphanumeric spacing and case.
4. **Convert Sentence Case**: Smart punctuation-based splitter capitalizing sentence start letters.
5. **Count Word Frequency**: Word extractor counting unique occurrences case-insensitively.
6. **Find Longest Word**: Finds the longest contiguous word in sentences.
7. **Remove Duplicate Characters**: Preserves order of first occurrence while removing subsequent matches.

#### List Challenges (`list_challenges.py`)
1. **Largest Number**: Dynamic search with empty list exception handling.
2. **Smallest Number**: Dynamic search with empty list exception handling.
3. **Remove Duplicates**: Order-preserving deduplication using key indices.
4. **Find Common Elements**: Computes intersection of lists, keeping original order.
5. **Count Even and Odd Numbers**: Category counts with empty input prevention.
6. **Second Largest Number**: Deduplicates and finds sub-maximum, handling lists with $< 2$ unique items.
7. **Manual Sorting Algorithm**: Custom Bubble Sort implementation supporting custom directions.

#### Dictionary Challenges (`dictionary_challenges.py`)
1. **Character Frequency Counter**: Character mapping.
2. **Merge Dictionaries**: Smart merger recursively traversing dictionaries, appending list elements, joining sets, summing matching numbers, and overwriting basic collisions.
3. **Find Maximum Value Key**: Checks largest value mapping, handling empty datasets.
4. **Student Marks Average Calculator**: Averages student scores, validating presence of data.
5. **Group Data by Category**: Groups dictionary list elements by a specified key.
6. **Word Frequency Counter**: Cleans and strips list strings to count frequencies.
7. **Nested Dictionary Analysis**: Recursive key finder traversing complex object trees.

### 2. Session Dashboard & CLI

The CLI incorporates a dashboard that displays live session info:
* Total Challenges Implemented ($21$)
* Categories Covered ($3$)
* Execution count tracking how many challenges have been invoked during the session.

### 3. Execution Logging (`logs/app.log`)

The logger registers:
* Application start and closure events.
* Navigation paths inside the console menus.
* Execution statistics (function name, category, input arguments, return value).
* Execution failures and exact stack trace error messages.

### 4. Exporting Reports (`reports/challenge_report.txt`)

Generated dynamically upon choosing option 5 (Exit) or running all examples. It formats a clean overview of execution stats, counts, and a complete history of runs including parameters, status (SUCCESS/FAILED), timestamps, and values.

---

## How to Run

1. Run the interactive menu system:
   ```bash
   python3 main.py
   ```
2. Navigate menus using numeric options:
   * **1, 2, 3**: Access categories to run specific challenges. You will be prompted to enter your own inputs or hit `Enter` to run with built-in test data.
   * **4**: Executes all $21$ challenge examples sequentially and exports a report.
   * **5**: Exports the final session execution report and exits.

---

## Testing Instructions

The toolkit includes a test suite with assertions verifying standard, border, and exception cases for all 21 functions.

You can execute tests with standard Python:
```bash
python3 test_challenges.py
```

Or run them with `pytest` for rich testing output:
```bash
pytest test_challenges.py
```

### Example Output from Tests:
```
.....................
----------------------------------------------------------------------
Ran 21 tests in 0.000s

OK
```

---

## Example Outputs

### Interactive CLI Main Menu
```
==================================================
          PYTHON PROBLEM SOLVING TOOLKIT          
==================================================
 Total Challenges Implemented : 21
 Categories Covered           : 3
 Functions Executed (Session) : 0
--------------------------------------------------
 1. String Challenges
 2. List Challenges
 3. Dictionary Challenges
 4. Run All Examples
 5. Exit
==================================================
Select an option (1-5): 
```

### Word Frequency Submenu Run
```
--- Running: Word Frequency Counter ---
Docstring: Count the frequency of each word in a list, case-insensitively and stripping whitespace.

Enter comma-separated words: apple, banana, apple, orange
Word Frequencies: {'apple': 2, 'banana': 1, 'orange': 1}
```

---

## Future Improvements

* **Algorithmic Optimizations**: Upgrade sorting algorithm to QuickSort or MergeSort ($O(N \log N)$ average complexity).
* **Data Serialization**: Add CSV/JSON import functionality for bulk test runner.
* **Parallel Execution**: Use Python's multiprocessing to evaluate heavy inputs concurrently.

---

## Author Information

* **Developer**: WeIntern Python Engineer Candidate
* **Role**: Week 1 Intern Task 3
* **Project**: Python Problem Solving Toolkit
