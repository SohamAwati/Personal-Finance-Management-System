from models.student import Student
from services.student_manager import StudentManager
from utils.formatter import display_students, display_statistics


def main():
    manager = StudentManager()

    # Add sample students
    manager.add_student(
        Student(
            101,
            "Soham",
            20,
            "Python",
            91
        )
    )

    manager.add_student(
        Student(
            102,
            "Rahul",
            21,
            "Data Science",
            82
        )
    )

    manager.add_student(
        Student(
            103,
            "Neha",
            19,
            "AI",
            96
        )
    )

    print("\nALL STUDENTS\n")

    display_students(
        manager.get_all_students()
    )

    print("\nSEARCH BY ID\n")

    student = manager.find_by_id(102)

    if student:
        print(student)

    print("\nSORT BY MARKS\n")

    display_students(
        manager.sort_by_marks()
    )

    print("\nSTATISTICS\n")

    stats = manager.get_statistics()

    display_statistics(stats)


if __name__ == "__main__":
    main()