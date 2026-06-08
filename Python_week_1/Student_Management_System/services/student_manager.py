# Student Manager Service

from typing import List, Optional

from models.student import Student
from storage.json_storage import JsonStorage
from utils.logger import logger

class StudentManager:
    def __init__(self):
        self.storage = JsonStorage()
        self.students: List[Student] = self.storage.load_students()

    def add_student(self, student : Student) -> bool:

        if self.find_by_id(student.student_id):
            logger.warning(
                f"Duplicate Student ID | ID={student.student_id}"
            )
            return False
        
        self.students.append(student)
        self.storage.save_students(self.students)

        logger.info(
            f"Student Added | ID={student.student_id} | Name={student.name}"
        )
        return True
    
    def get_all_students(self) -> List[Student]:
        return self.students.copy()
    
    def find_by_id(self, student_id: int) -> Optional[Student]:

        for student in self.students:
            if student.student_id == student_id:
                return student
            
        return None

    def find_by_name(self, name: str) -> List[Student]:

        results = []

        for student in self.students:
            if name.lower() in student.name.lower():
                results.append(student)

        return results

    def find_by_course(self, course: str) -> List[Student]:

        results = []

        for student in self.students:
            if course.lower() in student.course.lower():
                results.append(student)

        return results
    
    def update_student(
        self,
        student_id: int,
        name: str,
        age: int,
        course: str,
        marks: float
    ) -> bool:

        student = self.find_by_id(student_id)
        if not student:
            logger.warning(
                f"Update Failed - Student Not Found | ID={student_id}"
            )
            return False

        student.name = name
        student.age = age
        student.course = course
        student.marks = marks
        self.storage.save_students(self.students)

        logger.info(
            f"Student Updated | ID={student.student_id} | Name={student.name}"
        )

        return True
    
    def delete_student(self, student_id: int) -> bool:

        student = self.find_by_id(student_id)
        if not student:
            logger.warning(
                f"Delete Failed - Student Not Found | ID={student_id}"
            )
            return False

        self.students.remove(student)
        self.storage.save_students(self.students)

        logger.info(
            f"Student Deleted | ID={student.student_id} | Name={student.name}"
        )

        return True
    
    def sort_by_name(self) -> List[Student]:

        return sorted(
            self.students,
            key=lambda student: student.name.lower()
        )

    def sort_by_marks(self) -> List[Student]:

        return sorted(
            self.students,
            key=lambda student: student.marks,
            reverse=True
        )

    def sort_by_age(self) -> List[Student]:

        return sorted(
            self.students,
            key=lambda student: student.age
        )
    
    def get_statistics(self) -> dict:

        if not self.students:
            return {
                "total_students": 0,
                "average_marks": 0,
                "top_student": None,
                "lowest_student": None
            }

        average_marks = sum(
            student.marks for student in self.students
        ) / len(self.students)

        top_student = max(
            self.students,
            key=lambda student: student.marks
        )

        lowest_student = min(
            self.students,
            key=lambda student: student.marks
        )

        return {
            "total_students": len(self.students),
            "average_marks": round(average_marks, 2),
            "top_student": top_student,
            "lowest_student": lowest_student
        }