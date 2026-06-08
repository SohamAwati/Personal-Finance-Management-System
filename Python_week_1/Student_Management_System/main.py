from colorama import Fore, Style, init

from models.student import Student
from services.student_manager import StudentManager
from utils.formatter import (
    display_students,
    display_statistics
)
from utils.validator import(
    validate_student_id,
    validate_name,
    validate_age,
    validate_course,
    validate_marks
)

init(autoreset=True)

def show_menu():
    print("\n" + "=" * 55)

    print(
        Fore.CYAN +
        "Student Management System"
    )

    print("=" * 55)

    print("1. Add Student")
    print("2.View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Sort Students")
    print("7. Statistics Dashboard")
    print("8. Exit")

    print("=" * 55)

def add_student(manager):
    try:
        student_id = input("Enter Student ID: ")

        if not validate_student_id(student_id):
            print(Fore.RED + "Invalid ID")
            return

        name = input("Enter Name: ")

        if not validate_name(name):
            print(Fore.RED + "Invalid Name")
            return

        age = input("Enter Age: ")

        if not validate_age(age):
            print(Fore.RED + "Invalid Age")
            return

        course = input("Enter Course: ")

        if not validate_course(course):
            print(Fore.RED + "Invalid Course")
            return

        marks = input("Enter Marks: ")

        if not validate_marks(marks):
            print(Fore.RED + "Invalid Marks")
            return

        student = Student(
            student_id=int(student_id),
            name=name,
            age=int(age),
            course=course,
            marks=float(marks)
        )

        if manager.add_student(student):
            print(
                Fore.GREEN +
                "\n✓ Student Added Successfully"
            )
        else:
            print(
                Fore.RED +
                "\nStudent ID already exists"
            )

    except Exception as error:
        print(Fore.RED + str(error))    

def search_student(manager):

    print("\n1. Search by ID")
    print("2. Search by Name")
    print("3. Search by Course")

    choice = input("Choice: ")

    if choice == "1":

        student_id = int(
            input("Enter Student ID: ")
        )

        student = manager.find_by_id(student_id)

        if student:
            display_students([student])
        else:
            print(Fore.RED + "Student Not Found")

    elif choice == "2":

        name = input("Enter Name: ")

        results = manager.find_by_name(name)

        display_students(results)

    elif choice == "3":

        course = input("Enter Course: ")

        results = manager.find_by_course(course)

        display_students(results)

def sort_students(manager):

    print("\n1. Sort by Name")
    print("2. Sort by Marks")
    print("3. Sort by Age")

    choice = input("Choice: ")

    if choice == "1":
        display_students(
            manager.sort_by_name()
        )

    elif choice == "2":
        display_students(
            manager.sort_by_marks()
        )

    elif choice == "3":
        display_students(
            manager.sort_by_age()
        )

def update_student(manager):

    try:
        student_id = int(
            input("Enter Student ID to Update: ")
        )

        student = manager.find_by_id(student_id)

        if not student:
            print(Fore.RED + "Student not found.")
            return

        print("\nPress ENTER to keep current value.\n")

        name = input(
            f"Name [{student.name}]: "
        ).strip()

        age = input(
            f"Age [{student.age}]: "
        ).strip()

        course = input(
            f"Course [{student.course}]: "
        ).strip()

        marks = input(
            f"Marks [{student.marks}]: "
        ).strip()

        manager.update_student(
            student_id=student.student_id,
            name=name if name else student.name,
            age=int(age) if age else student.age,
            course=course if course else student.course,
            marks=float(marks) if marks else student.marks
        )

        print(
            Fore.GREEN +
            "✓ Student updated successfully."
        )

    except ValueError:
        print(Fore.RED + "Invalid input.")

def delete_student(manager):

    try:

        student_id = int(
            input("Enter Student ID: ")
        )

        student = manager.find_by_id(student_id)

        if not student:
            print(Fore.RED + "Student not found.")
            return

        print("\nSelected Student:")
        display_students([student])

        confirm = input(
            "\nAre you sure? (y/n): "
        ).lower()

        if confirm != "y":
            print(
                Fore.YELLOW +
                "Deletion cancelled."
            )
            return

        manager.delete_student(student_id)

        print(
            Fore.GREEN +
            "✓ Student deleted successfully."
        )

    except ValueError:
        print(Fore.RED + "Invalid ID.")

def main():

    manager = StudentManager()

    while True:

        show_menu()

        choice = input(
            "\nEnter Choice: "
        )

        if choice == "1":
            add_student(manager)

        elif choice == "2":
            display_students(
                manager.get_all_students()
            )

        elif choice == "3":
            search_student(manager)

        elif choice == "4":
            # update function
            update_student(manager)

        elif choice == "5":
            # delete function
            delete_student(manager)

        elif choice == "6":
            sort_students(manager)

        elif choice == "7":
            stats = manager.get_statistics()
            display_statistics(stats)

        elif choice == "8":

            print(
                Fore.GREEN +
                "\nThank you for using SIMS!"
            )

            break

        else:
            print(
                Fore.RED +
                "Invalid Choice"
            )


if __name__ == "__main__":
    main() 