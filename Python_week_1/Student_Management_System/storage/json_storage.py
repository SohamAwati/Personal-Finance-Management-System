# JSON Storage Module
#Handles loading and saving student recoreds

import json
from pathlib import Path
from typing import List

from models.student import Student

class JsonStorage:

    def __init__(self, file_path: str = "data/students.json"):
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file)

    def save_students(self, students: List[Student]) -> None:
        try:
            data = [student.to_dict() for student in students]

            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"Error saving students: {e}")
            
    def load_students(self) -> List[Student]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                return [Student.from_dict(item) for item in data]
            
        except Exception as e:
            print("Warning: Corrupted JSON file.")

            return []

        except Exception as e:

            print(f"Error loading data: {e}")

            return []