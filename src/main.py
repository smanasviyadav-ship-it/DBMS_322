"""Main Application Module

This is the main entry point for the Student Management System.
It provides a command-line interface for managing students, courses, and enrollments.
"""

from db_connection import db
from student import Student
from course import Course
from enrollment import Enrollment
from reports import Reports
import sys


def print_menu():
    """Display the main menu."""
    print("\n" + "="*60)
    print("STUDENT MANAGEMENT SYSTEM")
    print("="*60)
    print("\n1. Student Management")
    print("2. Course Management")
    print("3. Enrollment Management")
    print("4. Reports")
    print("5. Exit")
    print("\n" + "-"*60)


def student_menu():
    """Display student management menu."""
    while True:
        print("\n--- STUDENT MANAGEMENT ---")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. Search Student")
        print("5. View All Students")
        print("6. Back to Main Menu")
        choice = input("\nEnter your choice: ").strip()

        if choice == '1':
            print("\n--- ADD STUDENT ---")
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            gender = input("Gender (Male/Female/Other): ").strip()
            dob = input("Date of Birth (YYYY-MM-DD): ").strip()
            email = input("Email: ").strip()
            phone = input("Phone: ").strip()

            result = Student.add_student(first_name, last_name, gender, dob, email, phone)
            print(f"\n{'✓' if result['success'] else '✗'} {result['message']}")

        elif choice == '2':
            print("\n--- UPDATE STUDENT ---")
            student_id = input("Student ID: ").strip()
            if not student_id.isdigit():
                print("✗ Invalid Student ID")
                continue

            student = Student.get_student_by_id(int(student_id))
            if not student:
                print("✗ Student not found")
                continue

            print(f"Current: {student['first_name']} {student['last_name']} - {student['email']}")
            print("Leave blank to keep current value")

            updates = {}
            first_name = input(f"First Name [{student['first_name']}]: ").strip()
            if first_name:
                updates['first_name'] = first_name

            last_name = input(f"Last Name [{student['last_name']}]: ").strip()
            if last_name:
                updates['last_name'] = last_name

            email = input(f"Email [{student['email']}]: ").strip()
            if email:
                updates['email'] = email

            phone = input(f"Phone [{student['phone']}]: ").strip()
            if phone:
                updates['phone'] = phone

            if updates:
                result = Student.update_student(int(student_id), **updates)
                print(f"\n{'✓' if result['success'] else '✗'} {result['message']}")
            else:
                print("\nNo updates provided")

        elif choice == '3':
            print("\n--- DELETE STUDENT ---")
            student_id = input("Student ID: ").strip()
            if not student_id.isdigit():
                print("✗ Invalid Student ID")
                continue

            confirm = input("Are you sure? (yes/no): ").strip().lower()
            if confirm == 'yes':
                result = Student.delete_student(int(student_id))
                print(f"\n{'✓' if result['success'] else '✗'} {result['message']}")
            else:
                print("\nOperation cancelled")

        elif choice == '4':
            print("\n--- SEARCH STUDENT ---")
            print("Search by: 1. ID, 2. Email, 3. Name")
            search_type = input("Enter option: ").strip()

            results = []
            if search_type == '1':
                student_id = input("Student ID: ").strip()
                if student_id.isdigit():
                    results = Student.search_student(student_id=int(student_id))
            elif search_type == '2':
                email = input("Email: ").strip()
                results = Student.search_student(email=email)
            elif search_type == '3':
                first_name = input("First Name (optional): ").strip()
                last_name = input("Last Name (optional): ").strip()
                results = Student.search_student(first_name=first_name, last_name=last_name)

            if results:
                print("\n--- SEARCH RESULTS ---")
                for student in results:
                    print(f"ID: {student['student_id']} | {student['first_name']} {student['last_name']} | {student['email']}")
            else:
                print("\n✗ No students found")

        elif choice == '5':
            print("\n--- ALL STUDENTS ---")
            students = Student.get_all_students()
            if students:
                print(f"\n{'ID':<5} {'Name':<25} {'Email':<30} {'Phone':<15}")
                print("-" * 75)
                for student in students:
                    name = f"{student['first_name']} {student['last_name']}"
                    print(f"{student['student_id']:<5} {name:<25} {student['email']:<30} {student['phone']:<15}")
            else:
                print("\n✗ No students in database")

        elif choice == '6':
            break
        else:
            print("\n✗ Invalid choice")


def course_menu():
    """Display course management menu."""
    while True:
        print("\n--- COURSE MANAGEMENT ---")
        print("1. Add Course")
        print("2. Update Course")
        print("3. Delete Course")
        print("4. Search Course")
        print("5. View All Courses")
        print("6. Back to Main Menu")
        choice = input("\nEnter your choice: ").strip()

        if choice == '1':
            print("\n--- ADD COURSE ---")
            course_name = input("Course Name: ").strip()
            credits = input("Credits: ").strip()

            result = Course.add_course(course_name, credits)
            print(f"\n{'✓' if result['success'] else '✗'} {result['message']}")

        elif choice == '2':
            print("\n--- UPDATE COURSE ---")
            course_id = input("Course ID: ").strip()
            if not course_id.isdigit():
                print("✗ Invalid Course ID")
                continue

            course = Course.get_course_by_id(int(course_id))
            if not course:
                print("✗ Course not found")
                continue

            print(f"Current: {course['course_name']} ({course['credits']} credits)")
            print("Leave blank to keep current value")

            course_name = input(f"Course Name [{course['course_name']}]: ").strip()
            credits_input = input(f"Credits [{course['credits']}]: ").strip()

            updates = {}
            if course_name:
                updates['course_name'] = course_name
            if credits_input:
                updates['credits'] = credits_input

            if updates:
                result = Course.update_course(int(course_id), **updates)
                print(f"\n{'✓' if result['success'] else '✗'} {result['message']}")
            else:
                print("\nNo updates provided")

        elif choice == '3':
            print("\n--- DELETE COURSE ---")
            course_id = input("Course ID: ").strip()
            if not course_id.isdigit():
                print("✗ Invalid Course ID")
                continue

            confirm = input("Are you sure? (yes/no): ").strip().lower()
            if confirm == 'yes':
                result = Course.delete_course(int(course_id))
                print(f"\n{'✓' if result['success'] else '✗'} {result['message']}")
            else:
                print("\nOperation cancelled")

        elif choice == '4':
            print("\n--- SEARCH COURSE ---")
            print("Search by: 1. ID, 2. Name")
            search_type = input("Enter option: ").strip()

            results = []
            if search_type == '1':
                course_id = input("Course ID: ").strip()
                if course_id.isdigit():
                    results = Course.search_course(course_id=int(course_id))
            elif search_type == '2':
                course_name = input("Course Name: ").strip()
                results = Course.search_course(course_name=course_name)

            if results:
                print("\n--- SEARCH RESULTS ---")
                for course in results:
                    print(f"ID: {course['course_id']} | {course['course_name']} | {course['credits']} credits")
            else:
                print("\n✗ No courses found")

        elif choice == '5':
            print("\n--- ALL COURSES ---")
            courses = Course.get_all_courses()
            if courses:
                print(f"\n{'ID':<5} {'Course Name':<40} {'Credits':<8}")
                print("-" * 53)
                for course in courses:
                    print(f"{course['course_id']:<5} {course['course_name']:<40} {course['credits']:<8}")
            else:
                print("\n✗ No courses in database")

        elif choice == '6':
            break
        else:
            print("\n✗ Invalid choice")


def enrollment_menu():
    """Display enrollment management menu."""
    while True:
        print("\n--- ENROLLMENT MANAGEMENT ---")
        print("1. Enroll Student in Course")
        print("2. Remove Enrollment")
        print("3. View Student's Courses")
        print("4. View Course's Students")
        print("5. View All Enrollments")
        print("6. Back to Main Menu")
        choice = input("\nEnter your choice: ").strip()

        if choice == '1':
            print("\n--- ENROLL STUDENT ---")
            student_id = input("Student ID: ").strip()
            course_id = input("Course ID: ").strip()

            if student_id.isdigit() and course_id.isdigit():
                result = Enrollment.enroll_student(int(student_id), int(course_id))
                print(f"\n{'✓' if result['success'] else '✗'} {result['message']}")
            else:
                print("\n✗ Invalid IDs")

        elif choice == '2':
            print("\n--- REMOVE ENROLLMENT ---")
            enrollment_id = input("Enrollment ID: ").strip()
            if enrollment_id.isdigit():
                confirm = input("Are you sure? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    result = Enrollment.remove_enrollment(int(enrollment_id))
                    print(f"\n{'✓' if result['success'] else '✗'} {result['message']}")
                else:
                    print("\nOperation cancelled")
            else:
                print("\n✗ Invalid Enrollment ID")

        elif choice == '3':
            print("\n--- VIEW STUDENT'S COURSES ---")
            student_id = input("Student ID: ").strip()
            if student_id.isdigit():
                enrollments = Enrollment.get_enrollments_by_student(int(student_id))
                if enrollments:
                    print(f"\n{'Enrollment ID':<15} {'Course Name':<40} {'Credits':<8} {'Date':<12}")
                    print("-" * 75)
                    for enrollment in enrollments:
                        print(f"{enrollment['enrollment_id']:<15} {enrollment['course_name']:<40} {enrollment['credits']:<8} {enrollment['enrollment_date']}")
                else:
                    print("\n✗ Student not found or not enrolled in any courses")
            else:
                print("\n✗ Invalid Student ID")

        elif choice == '4':
            print("\n--- VIEW COURSE'S STUDENTS ---")
            course_id = input("Course ID: ").strip()
            if course_id.isdigit():
                enrollments = Enrollment.get_enrollments_by_course(int(course_id))
                if enrollments:
                    print(f"\n{'Student ID':<12} {'Name':<25} {'Email':<30} {'Date':<12}")
                    print("-" * 79)
                    for enrollment in enrollments:
                        name = f"{enrollment['first_name']} {enrollment['last_name']}"
                        print(f"{enrollment['student_id']:<12} {name:<25} {enrollment['email']:<30} {enrollment['enrollment_date']}")
                else:
                    print("\n✗ Course not found or no enrollments")
            else:
                print("\n✗ Invalid Course ID")

        elif choice == '5':
            print("\n--- ALL ENROLLMENTS ---")
            enrollments = Enrollment.get_all_enrollments()
            if enrollments:
                print(f"\n{'ID':<8} {'Student':<25} {'Course Name':<40} {'Date':<12}")
                print("-" * 85)
                for enrollment in enrollments:
                    name = f"{enrollment['first_name']} {enrollment['last_name']}"
                    print(f"{enrollment['enrollment_id']:<8} {name:<25} {enrollment['course_name']:<40} {enrollment['enrollment_date']}")
            else:
                print("\n✗ No enrollments in database")

        elif choice == '6':
            break
        else:
            print("\n✗ Invalid choice")


def reports_menu():
    """Display reports menu."""
    while True:
        print("\n--- REPORTS ---")
        print("1. Summary Report")
        print("2. Student Enrollment Report")
        print("3. Course Enrollment Report")
        print("4. Student Total Credits")
        print("5. Back to Main Menu")
        choice = input("\nEnter your choice: ").strip()

        if choice == '1':
            Reports.print_summary_report()

        elif choice == '2':
            print("\n--- STUDENT ENROLLMENT REPORT ---")
            report = Reports.get_student_enrollment_report()
            if report:
                print(f"\n{'ID':<5} {'Name':<25} {'Email':<30} {'Courses':<8} {'Enrolled In':<40}")
                print("-" * 110)
                for row in report:
                    name = f"{row['first_name']} {row['last_name']}"
                    courses = row['courses'] if row['courses'] else 'None'
                    print(f"{row['student_id']:<5} {name:<25} {row['email']:<30} {row['enrolled_courses']:<8} {courses:<40}")
            else:
                print("\n✗ No data available")

        elif choice == '3':
            print("\n--- COURSE ENROLLMENT REPORT ---")
            report = Reports.get_course_enrollment_report()
            if report:
                print(f"\n{'ID':<5} {'Course Name':<40} {'Credits':<8} {'Students':<10} {'Enrolled Students':<30}")
                print("-" * 93)
                for row in report:
                    students = row['students'] if row['students'] else 'None'
                    print(f"{row['course_id']:<5} {row['course_name']:<40} {row['credits']:<8} {row['total_students']:<10} {students:<30}")
            else:
                print("\n✗ No data available")

        elif choice == '4':
            print("\n--- STUDENT TOTAL CREDITS ---")
            report = Reports.get_total_credits_by_student()
            if report:
                print(f"\n{'ID':<5} {'Name':<25} {'Total Credits':<15} {'Total Courses':<15}")
                print("-" * 60)
                for row in report:
                    name = f"{row['first_name']} {row['last_name']}"
                    total_credits = row['total_credits'] if row['total_credits'] else 0
                    print(f"{row['student_id']:<5} {name:<25} {total_credits:<15} {row['total_courses']:<15}")
            else:
                print("\n✗ No data available")

        elif choice == '5':
            break
        else:
            print("\n✗ Invalid choice")


def main():
    """Main application loop."""
    # Connect to database
    if not db.connect():
        print("\n✗ Failed to connect to database. Please check your database configuration.")
        print("\nMake sure:")
        print("1. MySQL server is running")
        print("2. Database 'student_management_system' exists")
        print("3. Environment variables are set correctly in .env file")
        sys.exit(1)

    try:
        while True:
            print_menu()
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                student_menu()
            elif choice == '2':
                course_menu()
            elif choice == '3':
                enrollment_menu()
            elif choice == '4':
                reports_menu()
            elif choice == '5':
                print("\n✓ Thank you for using Student Management System")
                break
            else:
                print("\n✗ Invalid choice. Please try again.")
    finally:
        db.disconnect()


if __name__ == "__main__":
    main()
