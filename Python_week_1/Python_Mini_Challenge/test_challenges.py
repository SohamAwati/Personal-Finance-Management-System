import unittest
from string_challenges import (
    reverse_string,
    count_vowels,
    is_palindrome,
    convert_to_sentence_case,
    count_word_frequency,
    find_longest_word,
    remove_duplicate_characters,
)
from list_challenges import (
    find_largest,
    find_smallest,
    remove_duplicates,
    find_common_elements,
    count_even_odd,
    find_second_largest,
    manual_sort,
)
from dictionary_challenges import (
    count_char_frequency,
    merge_dictionaries,
    find_max_value_key,
    calculate_student_averages,
    group_by_category,
    count_word_frequency_dict,
    analyze_nested_dict,
)


class TestStringChallenges(unittest.TestCase):

    def test_reverse_string(self):
        self.assertEqual(reverse_string("python"), "nohtyp")
        self.assertEqual(reverse_string(""), "")
        self.assertEqual(reverse_string("a"), "a")

    def test_count_vowels(self):
        self.assertEqual(count_vowels("python"), 1)
        self.assertEqual(count_vowels("aeiouAEIOU"), 10)
        self.assertEqual(count_vowels("bcdfghjklmnpqrstvwxyz"), 0)
        self.assertEqual(count_vowels(""), 0)

    def test_is_palindrome(self):
        self.assertTrue(is_palindrome("madam"))
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama"))
        self.assertFalse(is_palindrome("python"))
        self.assertTrue(is_palindrome(""))

    def test_convert_to_sentence_case(self):
        self.assertEqual(
            convert_to_sentence_case("hello world. this is python."),
            "Hello world. This is python.",
        )
        self.assertEqual(
            convert_to_sentence_case("wow! what a day? indeed."),
            "Wow! What a day? Indeed.",
        )
        self.assertEqual(convert_to_sentence_case(""), "")

    def test_count_word_frequency(self):
        self.assertEqual(
            count_word_frequency("Hello world! Hello again."),
            {"hello": 2, "world": 1, "again": 1},
        )
        self.assertEqual(count_word_frequency(""), {})

    def test_find_longest_word(self):
        self.assertEqual(
            find_longest_word("Find the longest word in this sentence."),
            "sentence",
        )
        self.assertEqual(find_longest_word(""), "")

    def test_remove_duplicate_characters(self):
        self.assertEqual(remove_duplicate_characters("programming"), "progamin")
        self.assertEqual(remove_duplicate_characters(""), "")


class TestListChallenges(unittest.TestCase):

    def test_find_largest(self):
        self.assertEqual(find_largest([1, 5, 3]), 5)
        self.assertEqual(find_largest([-10, -5, -20]), -5)
        with self.assertRaises(ValueError):
            find_largest([])

    def test_find_smallest(self):
        self.assertEqual(find_smallest([1, 5, 3]), 1)
        self.assertEqual(find_smallest([-10, -5, -20]), -20)
        with self.assertRaises(ValueError):
            find_smallest([])

    def test_remove_duplicates(self):
        self.assertEqual(remove_duplicates([1, 2, 2, 3]), [1, 2, 3])
        self.assertEqual(remove_duplicates([]), [])

    def test_find_common_elements(self):
        self.assertEqual(find_common_elements([1, 2, 3], [2, 3, 4]), [2, 3])
        self.assertEqual(find_common_elements([1, 1, 2], [1, 3]), [1])
        self.assertEqual(find_common_elements([], [1, 2]), [])

    def test_count_even_odd(self):
        self.assertEqual(count_even_odd([1, 2, 3, 4]), {"even": 2, "odd": 2})
        with self.assertRaises(ValueError):
            count_even_odd([])

    def test_find_second_largest(self):
        self.assertEqual(find_second_largest([1, 5, 5, 3]), 3)
        with self.assertRaises(ValueError):
            find_second_largest([1])
        with self.assertRaises(ValueError):
            find_second_largest([1, 1, 1])

    def test_manual_sort(self):
        self.assertEqual(manual_sort([3, 1, 4]), [1, 3, 4])
        self.assertEqual(manual_sort([3, 1, 4], ascending=False), [4, 3, 1])
        self.assertEqual(manual_sort([]), [])


class TestDictionaryChallenges(unittest.TestCase):

    def test_count_char_frequency(self):
        self.assertEqual(
            count_char_frequency("hello"), {"h": 1, "e": 1, "l": 2, "o": 1}
        )
        self.assertEqual(count_char_frequency(""), {})

    def test_merge_dictionaries(self):
        dict1 = {"a": 1, "b": [1, 2], "c": {"x": 10}}
        dict2 = {"b": [3], "c": {"y": 20}, "d": 4}
        expected = {"a": 1, "b": [1, 2, 3], "c": {"x": 10, "y": 20}, "d": 4}
        self.assertEqual(merge_dictionaries(dict1, dict2), expected)

    def test_find_max_value_key(self):
        self.assertEqual(
            find_max_value_key({"apple": 10, "banana": 15}), "banana"
        )
        with self.assertRaises(ValueError):
            find_max_value_key({})

    def test_calculate_student_averages(self):
        students = {"Alice": [80, 90], "Bob": [70, 85]}
        self.assertEqual(
            calculate_student_averages(students), {"Alice": 85.0, "Bob": 77.5}
        )
        with self.assertRaises(ValueError):
            calculate_student_averages({"Charlie": []})

    def test_group_by_category(self):
        data = [
            {"name": "Apple", "type": "Fruit"},
            {"name": "Carrot", "type": "Veg"},
        ]
        expected = {
            "Fruit": [{"name": "Apple", "type": "Fruit"}],
            "Veg": [{"name": "Carrot", "type": "Veg"}],
        }
        self.assertEqual(group_by_category(data, "type"), expected)

    def test_count_word_frequency_dict(self):
        self.assertEqual(
            count_word_frequency_dict(["apple ", " Apple", "banana"]),
            {"apple": 2, "banana": 1},
        )
        self.assertEqual(count_word_frequency_dict([]), {})

    def test_analyze_nested_dict(self):
        self.assertEqual(
            analyze_nested_dict({"a": 1, "nested": {"a": 2, "b": 3}}, "a"),
            [1, 2],
        )
        self.assertEqual(analyze_nested_dict({"a": 1}, "b"), [])


if __name__ == "__main__":
    unittest.main()
