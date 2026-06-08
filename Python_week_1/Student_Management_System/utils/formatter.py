#Formatting utility

from typing import List
from tabulate import tabulate
from colorama import Fore, Style

from models.student import Student

def display_students(students: List[Student]) -> None:
    if not students:
        print("No students to display.")
        return
    
    table = []

    for student in students:
        table.append([
            student.student_id, 
            student.name,
            student.age,
            student.course,
            student.marks
        ])

    print(tabulate(
        table,
        headers = ["ID", "Name", "Age", "Course", "Marks"],
        tablefmt = "grid"
    ))

def display_statistics(stats: dict) -> None:
    
    print("\n" + "=" * 40)
    print(Fore.CYAN + "STUDENT ANALYTICS DASHBOARD")
    print("=" * 40)

    print(f"Total Students: {stats['total_students']}")
    print(f"Average Marks: {stats['average_marks']}")

    if stats["top_student"]:
        print(
            Fore.GREEN + 
            f"Top Performer : "
            f"{stats['top_student'].name} "
            f"({stats['top_student'].marks}) "
        )

    if stats["lowest_student"]:
        print(
            Fore.GREEN + 
            f"Lowest Performer : "
            f"{stats['lowest_student'].name} "
            f"({stats['lowest_student'].marks}) "
        )