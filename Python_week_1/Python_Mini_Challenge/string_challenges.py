def reverse_string(text: str) -> str:
   
    return text[::-1]


def count_vowels(text: str) -> int:
   
    vowels = {"a", "e", "i", "o", "u", "A", "E", "I", "O", "U"}
    return sum(1 for char in text if char in vowels)


def is_palindrome(text: str) -> bool:

    cleaned = "".join(char.lower() for char in text if char.isalnum())
    return cleaned == cleaned[::-1]


def convert_to_sentence_case(text: str) -> str:
   
    if not text:
        return text

    import re
    parts = re.split(r"(\s*[\.\!\?]+\s*)", text)
    result = []
    capitalize_next = True
    for part in parts:
        if not part:
            continue
        if re.match(r"^\s*[\.\!\?]+\s*$", part):
            result.append(part)
            capitalize_next = True
        else:
            if capitalize_next:
                result.append(part.capitalize())
                capitalize_next = False
            else:
                result.append(part)
    return "".join(result)


def count_word_frequency(text: str) -> dict[str, int]:
    
    import re
    words = re.findall(r"\b\w+\b", text.lower())
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq


def find_longest_word(text: str) -> str:
    
    import re
    words = re.findall(r"\b\w+\b", text)
    if not words:
        return ""
    return max(words, key=len)


def remove_duplicate_characters(text: str) -> str:

    return "".join(dict.fromkeys(text))
