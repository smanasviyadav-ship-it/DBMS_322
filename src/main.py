"""Main Application Module

This is the main entry point for the Student Management System.
It provides a menu-driven interface for managing students, courses, and enrollments.
"""

import sys
from db_connection import DatabaseConnection
from student import Student
from course import Course
from enrollment import Enrollment
from reports import Reports


class StudentManagementSystem:
    """Main application class for the Student Management System."""

    def __init__(self):
        """Initialize the Student Management System."""
        self.db = DatabaseConnection()
        self.reports = Reports()
        self.running = True

    def display_main_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "="*60)
        print("     STUDENT MANAGEMENT SYSTEM")
        print("="*60)
        print("\n1. Student Management")
        print("2. Course Management")
        print("3. Enrollment Management")
        print("4. Generate Reports")
        print("5. Exit")
        print("-"*60)

    def student_management_menu(self) -> None:
        """Display student management menu."""
        while True:
            print("\n--- Student Management ---")
            print("1. Add Student")
            print("2. View All Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Back to Main Menu")
            print("-"*40)

            choice = input("Select an option: ").strip()

            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.view_all_students()
            elif choice == '3':
                self.search_student()
            elif choice == '4':
                self.update_student()
            elif choice == '5':
                self.delete_student()
            elif choice == '6':
                break
            else:
                print("✗ Invalid option. Please try again.")

    def course_management_menu(self) -> None:
        """Display course management menu."""
        while True:
            print("\n--- Course Management ---")
            print("1. Add Course")
            print("2. View All Courses")
            print("3. Search Course")
            print("4. Update Course")
            print("5. Delete Course")
            print("6. Back to Main Menu")
            print("-"*40)

            choice = input("Select an option: ").strip()

            if choice == '1':
                self.add_course()
            elif choice == '2':
                self.view_all_courses()
            elif choice == '3':
                self.search_course()
            elif choice == '4':
                self.update_course()
            elif choice == '5':
                self.delete_course()
            elif choice == '6':
                break
            else:
                print("✗ Invalid option. Please try again.")

    def enrollment_management_menu(self) -> None:
        """Display enrollment management menu."""
        while True:
            print("\n--- Enrollment Management ---")
            print("1. Enroll Student")
            print("2. View Student Courses")
            print("3. View Course Students")
            print("4. View All Enrollments")
            print("5. Remove Enrollment")
            print("6. Update Grade")
            print("7. Back to Main Menu")
            print("-"*40)

            choice = input("Select an option: ").strip()

            if choice == '1':
                self.enroll_student()
            elif choice == '2':
                self.view_student_courses()
            elif choice == '3':
                self.view_course_students()
            elif choice == '4':
                self.view_all_enrollments()
            elif choice == '5':
                self.remove_enrollment()
            elif choice == '6':
                self.update_grade()
            elif choice == '7':
                break
            else:
                print("✗ Invalid option. Please try again.")

    def reports_menu(self) -> None:
        """Display reports menu."""
        while True:
            print("\n--- Reports ---")
            print("1. System Statistics")
            print("2. Student Enrollment Report")
            print("3. Course Enrollment Report")
            print("4. Top Enrolled Courses")
            print("5. Grade Distribution")
            print("6. Back to Main Menu")
            print("-"*40)

            choice = input("Select an option: ").strip()

            if choice == '1':
                self.display_system_statistics()
            elif choice == '2':
                self.display_student_enrollment_report()
            elif choice == '3':
                self.display_course_enrollment_report()
            elif choice == '4':
                self.display_top_courses()
            elif choice == '5':
                self.display_grade_distribution()
            elif choice == '6':
                break
            else:
                print("✗ Invalid option. Please try again.")

    # Student Management Methods
    def add_student(self) -> None:
        """Add a new student."""
        print("\n--- Add Student ---")
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        email = input("Email: ").strip()
        gender = input("Gender (Male/Female/Other) [optional]: ").strip() or None
        dob = input("Date of Birth (YYYY-MM-DD) [optional]: ").strip() or None
        phone = input("Phone [optional]: ").strip() or None

        student = Student(first_name, last_name, email, gender, dob, phone)
        student.add_student()

    def view_all_students(self) -> None:
        """Display all students."""
        print("\n--- All Students ---")
        students = Student.get_all_students()
        if not students:
            print("No students found.")
            return

        print(f"\n{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Email':<30} {'Phone':<15}")
        print("-"*80)
        for student in students:
            print(f"{student['student_id']:<5} {student['first_name']:<15} {student['last_name']:<15} {student['email']:<30} {student['phone'] or 'N/A':<15}")

    def search_student(self) -> None:
        """Search for a student."""
        print("\n--- Search Student ---")
        print("1. Search by ID")
        print("2. Search by Name")
        choice = input("Select search type: ").strip()

        if choice == '1':
            student_id = int(input("Enter Student ID: "))
            student = Student.get_student_by_id(student_id)
            if student:
                print(f"\nStudent ID: {student['student_id']}")
                print(f"Name: {student['first_name']} {student['last_name']}")
                print(f"Email: {student['email']}")
                print(f"Phone: {student['phone'] or 'N/A'}")
                print(f"Gender: {student['gender'] or 'N/A'}")
                print(f"DOB: {student['date_of_birth'] or 'N/A'}")
            else:
                print("✗ Student not found.")
        elif choice == '2':
            first_name = input("First Name [optional]: ").strip() or None
            last_name = input("Last Name [optional]: ").strip() or None
            students = Student.search_students_by_name(first_name, last_name)
            if students:
                print(f"\n{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Email':<30}")
                print("-"*65)
                for student in students:
                    print(f"{student['student_id']:<5} {student['first_name']:<15} {student['last_name']:<15} {student['email']:<30}")
            else:
                print("✗ No students found.")

    def update_student(self) -> None:
        """Update student information."""
        print("\n--- Update Student ---")
        student_id = int(input("Enter Student ID: "))
        student = Student.get_student_by_id(student_id)
        if not student:
            print("✗ Student not found.")
            return

        print(f"\nCurrent: {student['first_name']} {student['last_name']} ({student['email']})")
        first_name = input("New First Name [leave blank to keep]: ").strip() or None
        last_name = input("New Last Name [leave blank to keep]: ").strip() or None
        email = input("New Email [leave blank to keep]: ").strip() or None
        phone = input("New Phone [leave blank to keep]: ").strip() or None

        Student.update_student(student_id, first_name=first_name, last_name=last_name, email=email, phone=phone)

    def delete_student(self) -> None:
        """Delete a student."""
        print("\n--- Delete Student ---")
        student_id = int(input("Enter Student ID: "))
        confirm = input(f"Are you sure you want to delete student {student_id}? (yes/no): ").strip().lower()
        if confirm == 'yes':
            Student.delete_student(student_id)

    # Course Management Methods
    def add_course(self) -> None:
        """Add a new course."""
        print("\n--- Add Course ---")
        course_name = input("Course Name: ").strip()
        credits = int(input("Credits (1-10): "))
        description = input("Description [optional]: ").strip() or None

        course = Course(course_name, credits, description)
        course.add_course()

    def view_all_courses(self) -> None:
        """Display all courses."""
        print("\n--- All Courses ---")
        courses = Course.get_all_courses()
        if not courses:
            print("No courses found.")
            return

        print(f"\n{'ID':<5} {'Course Name':<40} {'Credits':<8} {'Description':<25}")
        print("-"*80)
        for course in courses:
            desc = (course['description'][:22] + '...') if course['description'] and len(course['description']) > 25 else course['description'] or 'N/A'
            print(f"{course['course_id']:<5} {course['course_name']:<40} {course['credits']:<8} {desc:<25}")

    def search_course(self) -> None:
        """Search for a course."""
        print("\n--- Search Course ---")
        course_name = input("Enter Course Name (partial match): ").strip()
        courses = Course.search_courses_by_name(course_name)
        if courses:
            print(f"\n{'ID':<5} {'Course Name':<40} {'Credits':<8}")
            print("-"*55)
            for course in courses:
                print(f"{course['course_id']:<5} {course['course_name']:<40} {course['credits']:<8}")
        else:
            print("✗ No courses found.")

    def update_course(self) -> None:
        """Update course information."""
        print("\n--- Update Course ---")
        course_id = int(input("Enter Course ID: "))
        course = Course.get_course_by_id(course_id)
        if not course:
            print("✗ Course not found.")
            return

        print(f"\nCurrent: {course['course_name']} ({course['credits']} credits)")
        course_name = input("New Course Name [leave blank to keep]: ").strip() or None
        credits = input("New Credits [leave blank to keep]: ").strip()
        credits = int(credits) if credits else None
        description = input("New Description [leave blank to keep]: ").strip() or None

        Course.update_course(course_id, course_name=course_name, credits=credits, description=description)

    def delete_course(self) -> None:
        """Delete a course."""
        print("\n--- Delete Course ---")
        course_id = int(input("Enter Course ID: "))
        confirm = input(f"Are you sure you want to delete course {course_id}? (yes/no): ").strip().lower()
        if confirm == 'yes':
            Course.delete_course(course_id)

    # Enrollment Management Methods
    def enroll_student(self) -> None:
        """Enroll a student in a course."""
        print("\n--- Enroll Student ---")
        student_id = int(input("Enter Student ID: "))
        course_id = int(input("Enter Course ID: "))
        enrollment_date = input("Enrollment Date (YYYY-MM-DD) [optional]: ").strip() or None

        enrollment = Enrollment(student_id, course_id, enrollment_date)
        enrollment.enroll_student()

    def view_student_courses(self) -> None:
        """View courses for a student."""
        print("\n--- View Student Courses ---")
        student_id = int(input("Enter Student ID: "))
        courses = Enrollment.get_student_courses(student_id)
        if not courses:
            print("No enrollments found for this student.")
            return

        print(f"\n{'Course ID':<10} {'Course Name':<40} {'Enrollment Date':<18} {'Grade':<8}")
        print("-"*80)
        for course in courses:
            print(f"{course['course_id']:<10} {course['course_name']:<40} {course['enrollment_date']:<18} {course['grade'] or 'Not Graded':<8}")

    def view_course_students(self) -> None:
        """View students in a course."""
        print("\n--- View Course Students ---")
        course_id = int(input("Enter Course ID: "))
        students = Enrollment.get_course_students(course_id)
        if not students:
            print("No students enrolled in this course.")
            return

        print(f"\n{'Student ID':<12} {'Name':<30} {'Email':<30} {'Grade':<8}")
        print("-"*80)
        for student in students:
            print(f"{student['student_id']:<12} {student['first_name'] + ' ' + student['last_name']:<30} {student['email']:<30} {student['grade'] or 'Not Graded':<8}")

    def view_all_enrollments(self) -> None:
        """View all enrollments."""
        print("\n--- All Enrollments ---")
        enrollments = Enrollment.get_all_enrollments()
        if not enrollments:
            print("No enrollments found.")
            return

        print(f"\n{'ID':<5} {'Student':<25} {'Course':<30} {'Date':<12} {'Grade':<8}")
        print("-"*85)
        for enrollment in enrollments:
            print(f"{enrollment['enrollment_id']:<5} {enrollment['student_name']:<25} {enrollment['course_name']:<30} {enrollment['enrollment_date']:<12} {enrollment['grade'] or 'Not Graded':<8}")

    def remove_enrollment(self) -> None:
        """Remove a student's enrollment."""
        print("\n--- Remove Enrollment ---")
        student_id = int(input("Enter Student ID: "))
        course_id = int(input("Enter Course ID: "))
        confirm = input(f"Remove student {student_id} from course {course_id}? (yes/no): ").strip().lower()
        if confirm == 'yes':
            Enrollment.remove_enrollment(student_id, course_id)

    def update_grade(self) -> None:
        """Update a student's grade."""
        print("\n--- Update Grade ---")
        student_id = int(input("Enter Student ID: "))
        course_id = int(input("Enter Course ID: "))
        grade = input("Enter Grade (A, A-, B+, B, B-, C+, C, C-, D, F): ").strip()
        Enrollment.update_grade(student_id, course_id, grade)

    # Reports Methods
    def display_system_statistics(self) -> None:
        """Display system statistics."""
        stats = self.reports.get_system_statistics()
        print("\n" + self.reports.export_report_to_text('system'))

    def display_student_enrollment_report(self) -> None:
        """Display student enrollment report."""
        print("\n" + self.reports.export_report_to_text('student_enrollment'))

    def display_course_enrollment_report(self) -> None:
        """Display course enrollment report."""
        print("\n" + self.reports.export_report_to_text('course_enrollment'))

    def display_top_courses(self) -> None:
        """Display top enrolled courses."""
        print("\n--- Top Enrolled Courses ---")
        courses = self.reports.get_top_enrolled_courses()
        print(f"\n{'Course ID':<12} {'Course Name':<40} {'Enrollments':<12}")
        print("-"*65)
        for course in courses:
            print(f"{course['course_id']:<12} {course['course_name']:<40} {course['enrollment_count']:<12}")

    def display_grade_distribution(self) -> None:
        """Display grade distribution."""
        print("\n--- Grade Distribution ---")
        distribution = self.reports.get_grade_distribution()
        print(f"\n{'Grade':<10} {'Count':<10}")
        print("-"*20)
        for grade, count in sorted(distribution.items()):
            print(f"{grade:<10} {count:<10}")

    def run(self) -> None:
        """Run the main application loop."""
        print("\n✓ Welcome to the Student Management System!")

        if not self.db.is_connected():
            print("✗ Failed to connect to database. Please check your database configuration.")
            sys.exit(1)

        while self.running:
            self.display_main_menu()
            choice = input("Select an option: ").strip()

            if choice == '1':
                self.student_management_menu()
            elif choice == '2':
                self.course_management_menu()
            elif choice == '3':
                self.enrollment_management_menu()
            elif choice == '4':
                self.reports_menu()
            elif choice == '5':
                print("\n✓ Thank you for using Student Management System!")
                self.db.disconnect()
                self.running = False
            else:
                print("✗ Invalid option. Please try again.")


if __name__ == "__main__":
    app = StudentManagementSystem()
    app.run()
