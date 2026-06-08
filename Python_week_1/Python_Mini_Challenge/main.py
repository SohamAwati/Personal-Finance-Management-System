import os
import re
import json
import logging
from datetime import datetime

import string_challenges
import list_challenges
import dictionary_challenges

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "app.log")

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("Toolkit")


class SessionTracker:

    def __init__(self) -> None:
        self.total_challenges = 21
        self.categories_covered = 3
        self.executed_functions: dict[str, int] = {}
        self.history: list[dict[str, any]] = []

    def record_execution(
        self,
        category: str,
        func_name: str,
        inputs: any,
        outputs: any,
        status: str = "SUCCESS",
    ) -> None:
        self.executed_functions[func_name] = (
            self.executed_functions.get(func_name, 0) + 1
        )
        self.history.append(
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "category": category,
                "function": func_name,
                "inputs": inputs,
                "outputs": outputs,
                "status": status,
            }
        )
        logger.info(
            f"Executed challenge: {func_name} | Category: {category} | Status: {status}"
        )

    def record_error(self, func_name: str, error_msg: str) -> None:
        logger.error(f"Error in {func_name}: {error_msg}")

    def get_total_executions(self) -> int:
        return sum(self.executed_functions.values())

    def export_report(self) -> str:
        report_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "reports"
        )
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, "challenge_report.txt")

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("==================================================\n")
            f.write("          PYTHON PROBLEM SOLVING TOOLKIT          \n")
            f.write("                EXECUTION REPORT                  \n")
            f.write("==================================================\n\n")
            f.write(
                f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            f.write(f"Total Challenges Implemented: {self.total_challenges}\n")
            f.write(f"Categories Covered: {self.categories_covered}\n")
            f.write(f"Total Invocations: {self.get_total_executions()}\n\n")

            f.write("--- Invocation Statistics ---\n")
            for func, count in self.executed_functions.items():
                f.write(f"- {func}: {count} time(s)\n")
            f.write("\n")

            f.write("--- Detailed Execution Summary ---\n")
            for i, record in enumerate(self.history, 1):
                f.write(
                    f"{i}. [{record['timestamp']}] {record['category']} -> {record['function']}\n"
                )
                f.write(f"   Status: {record['status']}\n")
                f.write(f"   Inputs: {json.dumps(record['inputs'], default=str)}\n")
                f.write(
                    f"   Outputs: {json.dumps(record['outputs'], default=str)}\n"
                )
                f.write("   ----------------------------------------------\n")

        return report_path


def run_challenge_safe(tracker: SessionTracker, category: str, func, *args, **kwargs):
    func_name = func.__name__
    try:
        result = func(*args, **kwargs)
        tracker.record_execution(
            category, func_name, {"args": args, "kwargs": kwargs}, result
        )
        return result, None
    except Exception as e:
        tracker.record_error(func_name, str(e))
        return None, e


def handle_string_challenge(tracker: SessionTracker, name: str, func) -> None:
    print(f"\n--- Running: {name} ---")
    print(f"Docstring: {func.__doc__.strip() if func.__doc__ else 'No description available'}")
    text = input("Enter input text (or press Enter to use a default sample): ")
    if not text:
        text = "Hello world! This is a test. Is it a palindrome? Madam, yes."
    print(f"Executing with input: '{text}'")
    result, err = run_challenge_safe(tracker, "String", func, text)
    if err:
        print(f"Error executing challenge: {err}")
    else:
        print(f"Result: {result}")
    input("\nPress Enter to continue...")


def parse_numeric_list(prompt: str) -> list[float]:
    user_input = input(prompt)
    if not user_input.strip():
        return []
    return [float(x.strip()) for x in user_input.split(",") if x.strip()]


def parse_int_list(prompt: str) -> list[int]:
    user_input = input(prompt)
    if not user_input.strip():
        return []
    return [int(x.strip()) for x in user_input.split(",") if x.strip()]


def handle_list_challenge(tracker: SessionTracker, choice: int) -> None:
    if choice == 1:
        print("\n--- Running: Find Largest Number ---")
        print(f"Docstring: {list_challenges.find_largest.__doc__.strip() if list_challenges.find_largest.__doc__ else 'No description available'}")
        nums = parse_numeric_list(
            "Enter comma-separated numbers (e.g., 3, 5, 1, 9): "
        )
        if not nums:
            nums = [10, -5, 34, 18, 9]
            print(f"Using default sample: {nums}")
        result, err = run_challenge_safe(
            tracker, "List", list_challenges.find_largest, nums
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"Largest Number: {result}")

    elif choice == 2:
        print("\n--- Running: Find Smallest Number ---")
        print(f"Docstring: {list_challenges.find_smallest.__doc__.strip() if list_challenges.find_smallest.__doc__ else 'No description available'}")
        nums = parse_numeric_list("Enter comma-separated numbers: ")
        if not nums:
            nums = [10, -5, 34, 18, 9]
            print(f"Using default sample: {nums}")
        result, err = run_challenge_safe(
            tracker, "List", list_challenges.find_smallest, nums
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"Smallest Number: {result}")

    elif choice == 3:
        print("\n--- Running: Remove Duplicates ---")
        print(f"Docstring: {list_challenges.remove_duplicates.__doc__.strip() if list_challenges.remove_duplicates.__doc__ else 'No description available'}")
        items_input = input(
            "Enter comma-separated items (e.g., apple, banana, apple): "
        )
        if not items_input.strip():
            items = ["apple", "banana", "apple", "cherry", "banana"]
            print(f"Using default sample: {items}")
        else:
            items = [x.strip() for x in items_input.split(",") if x.strip()]
        result, err = run_challenge_safe(
            tracker, "List", list_challenges.remove_duplicates, items
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"Result (duplicates removed): {result}")

    elif choice == 4:
        print("\n--- Running: Find Common Elements ---")
        print(
            f"Docstring: {list_challenges.find_common_elements.__doc__.strip() if list_challenges.find_common_elements.__doc__ else 'No description available'}"
        )
        inp1 = input("Enter first list (comma-separated): ")
        inp2 = input("Enter second list (comma-separated): ")
        if not inp1.strip() or not inp2.strip():
            list1 = [1, 2, 3, 4, 5]
            list2 = [3, 4, 5, 6, 7]
            print(
                f"Using default samples:\nList 1: {list1}\nList 2: {list2}"
            )
        else:
            list1 = [x.strip() for x in inp1.split(",") if x.strip()]
            list2 = [x.strip() for x in inp2.split(",") if x.strip()]
        result, err = run_challenge_safe(
            tracker, "List", list_challenges.find_common_elements, list1, list2
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"Common Elements: {result}")

    elif choice == 5:
        print("\n--- Running: Count Even and Odd Numbers ---")
        print(f"Docstring: {list_challenges.count_even_odd.__doc__.strip() if list_challenges.count_even_odd.__doc__ else 'No description available'}")
        nums = parse_int_list("Enter comma-separated integers: ")
        if not nums:
            nums = [1, 2, 3, 4, 5, 6, 7]
            print(f"Using default sample: {nums}")
        result, err = run_challenge_safe(
            tracker, "List", list_challenges.count_even_odd, nums
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"Result: {result}")

    elif choice == 6:
        print("\n--- Running: Find Second Largest Number ---")
        print(
            f"Docstring: {list_challenges.find_second_largest.__doc__.strip() if list_challenges.find_second_largest.__doc__ else 'No description available'}"
        )
        nums = parse_numeric_list("Enter comma-separated numbers: ")
        if not nums:
            nums = [10, -5, 34, 18, 9, 34]
            print(f"Using default sample: {nums}")
        result, err = run_challenge_safe(
            tracker, "List", list_challenges.find_second_largest, nums
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"Second Largest Number: {result}")

    elif choice == 7:
        print("\n--- Running: Manual Sorting Algorithm (Bubble Sort) ---")
        print(f"Docstring: {list_challenges.manual_sort.__doc__.strip() if list_challenges.manual_sort.__doc__ else 'No description available'}")
        nums = parse_numeric_list("Enter comma-separated numbers: ")
        order = (
            input("Sort ascending? (y/n, default: y): ").strip().lower() != "n"
        )
        if not nums:
            nums = [23, 1, 56, 3, 9, 12]
            print(f"Using default sample: {nums}")
        result, err = run_challenge_safe(
            tracker, "List", list_challenges.manual_sort, nums, order
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"Sorted List: {result}")

    input("\nPress Enter to continue...")


def handle_dict_challenge(tracker: SessionTracker, choice: int) -> None:
    if choice == 1:
        print("\n--- Running: Character Frequency Counter ---")
        print(
            f"Docstring: {dictionary_challenges.count_char_frequency.__doc__.strip() if dictionary_challenges.count_char_frequency.__doc__ else 'No description available'}"
        )
        text = input("Enter string: ")
        if not text:
            text = "abracadabra"
            print(f"Using default: '{text}'")
        result, err = run_challenge_safe(
            tracker,
            "Dictionary",
            dictionary_challenges.count_char_frequency,
            text,
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"Result: {result}")

    elif choice == 2:
        print("\n--- Running: Merge Dictionaries ---")
        print(
            f"Docstring: {dictionary_challenges.merge_dictionaries.__doc__.strip() if dictionary_challenges.merge_dictionaries.__doc__ else 'No description available'}"
        )
        print("Note: Default lists, sets, numbers are merged intelligently.")
        d1 = {"apples": 10, "fruits": ["banana"], "config": {"debug": True}}
        d2 = {
            "apples": 5,
            "fruits": ["mango"],
            "config": {"port": 8080},
            "active": True,
        }
        print(
            f"Merging default sample dictionaries:\nDict 1: {d1}\nDict 2: {d2}"
        )
        result, err = run_challenge_safe(
            tracker, "Dictionary", dictionary_challenges.merge_dictionaries, d1, d2
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"Merged Result: {result}")

    elif choice == 3:
        print("\n--- Running: Find Maximum Value Key ---")
        print(
            f"Docstring: {dictionary_challenges.find_max_value_key.__doc__.strip() if dictionary_challenges.find_max_value_key.__doc__ else 'No description available'}"
        )
        print("Format: key1:val1, key2:val2 (e.g., apple:10, banana:15)")
        user_input = input("Enter dictionary entries: ")
        if not user_input.strip():
            d = {"physics": 85, "math": 98, "chemistry": 90}
            print(f"Using default: {d}")
        else:
            try:
                d = {
                    k.strip(): float(v.strip())
                    for x in user_input.split(",")
                    for k, v in [x.split(":")]
                }
            except Exception as e:
                print(f"Invalid format. Error: {e}")
                return
        result, err = run_challenge_safe(
            tracker, "Dictionary", dictionary_challenges.find_max_value_key, d
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"Key with Max Value: {result}")

    elif choice == 4:
        print("\n--- Running: Student Marks Average Calculator ---")
        print(
            f"Docstring: {dictionary_challenges.calculate_student_averages.__doc__.strip() if dictionary_challenges.calculate_student_averages.__doc__ else 'No description available'}"
        )
        students = {
            "Alice": [85.0, 92.5, 88.0],
            "Bob": [79.0, 81.5, 90.0],
            "Charlie": [95.0, 98.0, 91.5],
        }
        print(f"Evaluating student average grades for standard class:\n{students}")
        result, err = run_challenge_safe(
            tracker,
            "Dictionary",
            dictionary_challenges.calculate_student_averages,
            students,
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"Averages: {result}")

    elif choice == 5:
        print("\n--- Running: Group Data by Category ---")
        print(
            f"Docstring: {dictionary_challenges.group_by_category.__doc__.strip() if dictionary_challenges.group_by_category.__doc__ else 'No description available'}"
        )
        data = [
            {"item": "Laptop", "category": "Electronics"},
            {"item": "Banana", "category": "Food"},
            {"item": "Headphones", "category": "Electronics"},
            {"item": "Apple", "category": "Food"},
            {"item": "Desk", "category": "Furniture"},
        ]
        print(f"Grouping data items by 'category' key:\nData: {data}")
        result, err = run_challenge_safe(
            tracker,
            "Dictionary",
            dictionary_challenges.group_by_category,
            data,
            "category",
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"Grouped Result:\n{json.dumps(result, indent=2)}")

    elif choice == 6:
        print("\n--- Running: Word Frequency Counter ---")
        print(
            f"Docstring: {dictionary_challenges.count_word_frequency_dict.__doc__.strip() if dictionary_challenges.count_word_frequency_dict.__doc__ else 'No description available'}"
        )
        inp = input("Enter comma-separated words: ")
        if not inp.strip():
            words = ["apple", "banana", "apple", "orange", "banana", "apple"]
            print(f"Using default list: {words}")
        else:
            words = [x.strip() for x in inp.split(",") if x.strip()]
        result, err = run_challenge_safe(
            tracker,
            "Dictionary",
            dictionary_challenges.count_word_frequency_dict,
            words,
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"Word Frequencies: {result}")

    elif choice == 7:
        print("\n--- Running: Nested Dictionary Analysis ---")
        print(
            f"Docstring: {dictionary_challenges.analyze_nested_dict.__doc__.strip() if dictionary_challenges.analyze_nested_dict.__doc__ else 'No description available'}"
        )
        nested = {
            "id": "root",
            "value": 10,
            "children": [
                {"id": "child1", "value": 5},
                {
                    "id": "child2",
                    "value": 8,
                    "sub": {"id": "grandchild", "value": 15},
                },
            ],
        }
        print(f"Searching nested structure for key 'id':\nNested Dict: {nested}")
        result, err = run_challenge_safe(
            tracker,
            "Dictionary",
            dictionary_challenges.analyze_nested_dict,
            nested,
            "id",
        )
        if err:
            print(f"Error: {err}")
        else:
            print(f"Found Values: {result}")

    input("\nPress Enter to continue...")


def run_all_examples(tracker: SessionTracker) -> None:
    print("\n==================================================")
    print("          RUNNING ALL CHALLENGE EXAMPLES          ")
    print("==================================================")

    print("\n--- Running String Challenges ---")
    run_challenge_safe(tracker, "String", string_challenges.reverse_string, "python")
    run_challenge_safe(tracker, "String", string_challenges.count_vowels, "Hello World")
    run_challenge_safe(
        tracker,
        "String",
        string_challenges.is_palindrome,
        "A man, a plan, a canal: Panama",
    )
    run_challenge_safe(
        tracker,
        "String",
        string_challenges.convert_to_sentence_case,
        "hello world. this is python.",
    )
    run_challenge_safe(
        tracker,
        "String",
        string_challenges.count_word_frequency,
        "Hello world! Hello again.",
    )
    run_challenge_safe(
        tracker,
        "String",
        string_challenges.find_longest_word,
        "Find the longest word in this sentence.",
    )
    run_challenge_safe(
        tracker,
        "String",
        string_challenges.remove_duplicate_characters,
        "programming",
    )
    print("Executed 7 String Challenges successfully.")

    print("\n--- Running List Challenges ---")
    run_challenge_safe(tracker, "List", list_challenges.find_largest, [1, 5, 3])
    run_challenge_safe(tracker, "List", list_challenges.find_smallest, [1, 5, 3])
    run_challenge_safe(
        tracker, "List", list_challenges.remove_duplicates, [1, 2, 2, 3]
    )
    run_challenge_safe(
        tracker, "List", list_challenges.find_common_elements, [1, 2, 3], [2, 3, 4]
    )
    run_challenge_safe(
        tracker, "List", list_challenges.count_even_odd, [1, 2, 3, 4]
    )
    run_challenge_safe(
        tracker, "List", list_challenges.find_second_largest, [1, 5, 5, 3]
    )
    run_challenge_safe(tracker, "List", list_challenges.manual_sort, [3, 1, 4])
    print("Executed 7 List Challenges successfully.")

    print("\n--- Running Dictionary Challenges ---")
    run_challenge_safe(
        tracker, "Dictionary", dictionary_challenges.count_char_frequency, "hello"
    )
    run_challenge_safe(
        tracker,
        "Dictionary",
        dictionary_challenges.merge_dictionaries,
        {"a": 1, "b": 2},
        {"b": 3, "c": 4},
    )
    run_challenge_safe(
        tracker,
        "Dictionary",
        dictionary_challenges.find_max_value_key,
        {"apple": 10, "banana": 15},
    )
    run_challenge_safe(
        tracker,
        "Dictionary",
        dictionary_challenges.calculate_student_averages,
        {"Alice": [80, 90], "Bob": [70, 85]},
    )
    run_challenge_safe(
        tracker,
        "Dictionary",
        dictionary_challenges.group_by_category,
        [
            {"name": "Apple", "type": "Fruit"},
            {"name": "Carrot", "type": "Veg"},
        ],
        "type",
    )
    run_challenge_safe(
        tracker,
        "Dictionary",
        dictionary_challenges.count_word_frequency_dict,
        ["apple ", " Apple", "banana"],
    )
    run_challenge_safe(
        tracker,
        "Dictionary",
        dictionary_challenges.analyze_nested_dict,
        {"a": 1, "nested": {"a": 2, "b": 3}},
        "a",
    )
    print("Executed 7 Dictionary Challenges successfully.")

    print("\nAll 21 examples executed. Report written to reports/challenge_report.txt.")
    report_file = tracker.export_report()
    input("\nPress Enter to return to main menu...")


def main() -> None:
    tracker = SessionTracker()
    logger.info("Toolkit application started.")

    while True:
        print("\n==================================================")
        print("          PYTHON PROBLEM SOLVING TOOLKIT          ")
        print("==================================================")
        print(f" Total Challenges Implemented : {tracker.total_challenges}")
        print(f" Categories Covered           : {tracker.categories_covered}")
        print(f" Functions Executed (Session) : {tracker.get_total_executions()}")
        print("--------------------------------------------------")
        print(" 1. String Challenges")
        print(" 2. List Challenges")
        print(" 3. Dictionary Challenges")
        print(" 4. Run All Examples")
        print(" 5. Exit")
        print("==================================================")

        choice = input("Select an option (1-5): ").strip()
        logger.info(f"Main menu selection: {choice}")

        if choice == "1":
            while True:
                print("\n--------------------------------------------------")
                print("                STRING CHALLENGES")
                print("--------------------------------------------------")
                print(" 1. Reverse a String")
                print(" 2. Count Vowels")
                print(" 3. Palindrome Check")
                print(" 4. Convert Sentence Case")
                print(" 5. Count Word Frequency")
                print(" 6. Find Longest Word")
                print(" 7. Remove Duplicate Characters")
                print(" 8. Back to Main Menu")
                print("--------------------------------------------------")

                sub_choice = input("Select a challenge (1-8): ").strip()
                logger.info(f"String challenges menu selection: {sub_choice}")

                if sub_choice == "8":
                    break
                elif sub_choice == "1":
                    handle_string_challenge(
                        tracker, "Reverse a String", string_challenges.reverse_string
                    )
                elif sub_choice == "2":
                    handle_string_challenge(
                        tracker, "Count Vowels", string_challenges.count_vowels
                    )
                elif sub_choice == "3":
                    handle_string_challenge(
                        tracker, "Palindrome Check", string_challenges.is_palindrome
                    )
                elif sub_choice == "4":
                    handle_string_challenge(
                        tracker,
                        "Convert Sentence Case",
                        string_challenges.convert_to_sentence_case,
                    )
                elif sub_choice == "5":
                    handle_string_challenge(
                        tracker,
                        "Count Word Frequency",
                        string_challenges.count_word_frequency,
                    )
                elif sub_choice == "6":
                    handle_string_challenge(
                        tracker,
                        "Find Longest Word",
                        string_challenges.find_longest_word,
                    )
                elif sub_choice == "7":
                    handle_string_challenge(
                        tracker,
                        "Remove Duplicate Characters",
                        string_challenges.remove_duplicate_characters,
                    )
                else:
                    print("Invalid option. Please choose 1-8.")

        elif choice == "2":
            while True:
                print("\n--------------------------------------------------")
                print("                 LIST CHALLENGES")
                print("--------------------------------------------------")
                print(" 1. Largest Number")
                print(" 2. Smallest Number")
                print(" 3. Remove Duplicates")
                print(" 4. Find Common Elements")
                print(" 5. Count Even and Odd Numbers")
                print(" 6. Second Largest Number")
                print(" 7. Manual Sorting Algorithm")
                print(" 8. Back to Main Menu")
                print("--------------------------------------------------")

                sub_choice = input("Select a challenge (1-8): ").strip()
                logger.info(f"List challenges menu selection: {sub_choice}")

                if sub_choice == "8":
                    break
                elif sub_choice in {"1", "2", "3", "4", "5", "6", "7"}:
                    handle_list_challenge(tracker, int(sub_choice))
                else:
                    print("Invalid option. Please choose 1-8.")

        elif choice == "3":
            while True:
                print("\n--------------------------------------------------")
                print("              DICTIONARY CHALLENGES")
                print("--------------------------------------------------")
                print(" 1. Character Frequency Counter")
                print(" 2. Merge Dictionaries")
                print(" 3. Find Maximum Value Key")
                print(" 4. Student Marks Average Calculator")
                print(" 5. Group Data by Category")
                print(" 6. Word Frequency Counter")
                print(" 7. Nested Dictionary Analysis")
                print(" 8. Back to Main Menu")
                print("--------------------------------------------------")

                sub_choice = input("Select a challenge (1-8): ").strip()
                logger.info(f"Dictionary challenges menu selection: {sub_choice}")

                if sub_choice == "8":
                    break
                elif sub_choice in {"1", "2", "3", "4", "5", "6", "7"}:
                    handle_dict_challenge(tracker, int(sub_choice))
                else:
                    print("Invalid option. Please choose 1-8.")

        elif choice == "4":
            run_all_examples(tracker)

        elif choice == "5":
            report_path = tracker.export_report()
            print(f"\nReport exported to {report_path}")
            print("Thank you for using the Python Problem Solving Toolkit!")
            logger.info("Toolkit application closed.")
            break
        else:
            print("Invalid selection. Please choose 1-5.")


if __name__ == "__main__":
    main()
