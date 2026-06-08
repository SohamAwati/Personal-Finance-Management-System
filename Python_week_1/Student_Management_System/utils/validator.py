#Validation Utility

import re

def validate_student_id(student_id: str) -> bool:
    return student_id.isdigit()

def validate_name(name: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z ]{2,50}", name.strip()))

def validate_age(age: str) -> bool:
    return age.isdigit() and 15 <= int(age) <=100

def validate_marks(marks: str) -> bool:
    try:
        value = float(marks)
        return 0 <= value <= 100
    except ValueError:
        return False
    
def validate_course(course: str) -> bool:
    return len(course.strip()) >=2