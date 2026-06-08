def count_char_frequency(text: str) -> dict[str, int]:

    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    return freq


def merge_dictionaries(dict1: dict, dict2: dict) -> dict:
 
    merged = dict(dict1)
    for key, val2 in dict2.items():
        if key in merged:
            val1 = merged[key]
            if isinstance(val1, dict) and isinstance(val2, dict):
                merged[key] = merge_dictionaries(val1, val2)
            elif isinstance(val1, list) and isinstance(val2, list):
                merged[key] = val1 + val2
            elif isinstance(val1, set) and isinstance(val2, set):
                merged[key] = val1 | val2
            elif isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                merged[key] = val1 + val2
            else:
                merged[key] = val2
        else:
            merged[key] = val2
    return merged


def find_max_value_key(d: dict[str, int | float]) -> str:

    if not d:
        raise ValueError("Cannot find the maximum key in an empty dictionary.")
    max_key = None
    max_val = float("-inf")
    for key, val in d.items():
        if val > max_val:
            max_val = val
            max_key = key
    return max_key


def calculate_student_averages(
    students: dict[str, list[int | float]]
) -> dict[str, float]:

    if not students:
        return {}
    averages = {}
    for student, marks in students.items():
        if not marks:
            raise ValueError(f"Student {student} has no marks listed.")
        averages[student] = sum(marks) / len(marks)
    return averages


def group_by_category(
    data: list[dict[str, any]], category_key: str
) -> dict[any, list[dict[str, any]]]:

    grouped = {}
    for item in data:
        val = item.get(category_key, None)
        if val not in grouped:
            grouped[val] = []
        grouped[val].append(item)
    return grouped


def count_word_frequency_dict(words: list[str]) -> dict[str, int]:

    freq = {}
    for word in words:
        cleaned = word.strip().lower()
        if cleaned:
            freq[cleaned] = freq.get(cleaned, 0) + 1
    return freq


def analyze_nested_dict(d: dict, target_key: str) -> list[any]:

    results = []
    for key, val in d.items():
        if key == target_key:
            results.append(val)
        if isinstance(val, dict):
            results.extend(analyze_nested_dict(val, target_key))
        elif isinstance(val, list):
            for item in val:
                if isinstance(item, dict):
                    results.extend(analyze_nested_dict(item, target_key))
    return results
