def find_largest(numbers: list[int | float]) -> int | float:

    if not numbers:
        raise ValueError("Cannot find the largest element of an empty list.")
    largest = numbers[0]
    for num in numbers[1:]:
        if num > largest:
            largest = num
    return largest


def find_smallest(numbers: list[int | float]) -> int | float:

    if not numbers:
        raise ValueError("Cannot find the smallest element of an empty list.")
    smallest = numbers[0]
    for num in numbers[1:]:
        if num < smallest:
            smallest = num
    return smallest


def remove_duplicates(items: list) -> list:

    return list(dict.fromkeys(items))


def find_common_elements(list1: list, list2: list) -> list:

    set2 = set(list2)
    seen = set()
    result = []
    for item in list1:
        if item in set2 and item not in seen:
            result.append(item)
            seen.add(item)
    return result


def count_even_odd(numbers: list[int]) -> dict[str, int]:

    if not numbers:
        raise ValueError("Cannot count even and odd numbers in an empty list.")
    evens = sum(1 for num in numbers if num % 2 == 0)
    odds = len(numbers) - evens
    return {"even": evens, "odd": odds}


def find_second_largest(numbers: list[int | float]) -> int | float:

    unique_numbers = remove_duplicates(numbers)
    if len(unique_numbers) < 2:
        raise ValueError("List must contain at least two unique elements.")

    first = second = float("-inf")
    for num in unique_numbers:
        if num > first:
            second = first
            first = num
        elif num > second:
            second = num
    return second


def manual_sort(
    numbers: list[int | float], ascending: bool = True
) -> list[int | float]:

    arr = list(numbers)
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if ascending:
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
            else:
                if arr[j] < arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr
