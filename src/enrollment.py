"""Enrollment Management Module

This module handles all enrollment-related operations including enroll, remove enrollment,
and retrieve enrollment information. It implements OOP principles with proper validation.
"""

from db_connection import DatabaseConnection
from datetime import datetime
from typing import List, Optional, Dict, Any


class Enrollment:
    """Class to manage enrollment records in the database."""

    def __init__(self, student_id: int, course_id: int, enrollment_date: str = None):
        """Initialize an Enrollment object.

        Args:
            student_id: ID of the student
            course_id: ID of the course
            enrollment_date: Date of enrollment (YYYY-MM-DD), defaults to today
        """
        self.student_id = student_id
        self.course_id = course_id
        self.enrollment_date = enrollment_date or datetime.now().strftime('%Y-%m-%d')
        self.db = DatabaseConnection()

    @staticmethod
    def validate_date(date_str: str) -> bool:
        """Validate date format (YYYY-MM-DD).

        Args:
            date_str: Date string to validate

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def enroll_student(self) -> bool:
        """Enroll a student in a course.

        Returns:
            bool: True if successful, False otherwise
        """
        # Validate inputs
        if not isinstance(self.student_id, int) or self.student_id <= 0:
            print("✗ Invalid student ID")
            return False

        if not isinstance(self.course_id, int) or self.course_id <= 0:
            print("✗ Invalid course ID")
            return False

        if not self.validate_date(self.enrollment_date):
            print("✗ Invalid enrollment date format. Use YYYY-MM-DD")
            return False

        # Check if student exists
        student = self.db.fetch_one(
            "SELECT student_id FROM students WHERE student_id = %s",
            (self.student_id,)
        )
        if not student:
            print("✗ Student not found")
            return False

        # Check if course exists
        course = self.db.fetch_one(
            "SELECT course_id FROM courses WHERE course_id = %s",
            (self.course_id,)
        )
        if not course:
            print("✗ Course not found")
            return False

        # Check if already enrolled
        existing = self.db.fetch_one(
            "SELECT enrollment_id FROM enrollments WHERE student_id = %s AND course_id = %s",
            (self.student_id, self.course_id)
        )
        if existing:
            print("✗ Student is already enrolled in this course")
            return False

        # Insert enrollment
        query = """
            INSERT INTO enrollments (student_id, course_id, enrollment_date)
            VALUES (%s, %s, %s)
        """
        params = (self.student_id, self.course_id, self.enrollment_date)

        if self.db.execute_query(query, params):
            print(f"✓ Student {self.student_id} enrolled in Course {self.course_id} successfully")
            return True
        else:
            print("✗ Failed to enroll student")
            return False

    @staticmethod
    def get_student_courses(student_id: int) -> List[Dict[str, Any]]:
        """Get all courses a student is enrolled in.

        Args:
            student_id: ID of the student

        Returns:
            List[Dict]: List of courses with enrollment details
        """
        db = DatabaseConnection()
        courses = []

        query = """
            SELECT c.course_id, c.course_name, c.credits, e.enrollment_date, e.grade
            FROM enrollments e
            JOIN courses c ON e.course_id = c.course_id
            WHERE e.student_id = %s
            ORDER BY c.course_id
        """
        results = db.fetch_all(query, (student_id,))

        for result in results:
            courses.append({
                'course_id': result[0],
                'course_name': result[1],
                'credits': result[2],
                'enrollment_date': result[3],
                'grade': result[4]
            })
        return courses

    @staticmethod
    def get_course_students(course_id: int) -> List[Dict[str, Any]]:
        """Get all students enrolled in a course.

        Args:
            course_id: ID of the course

        Returns:
            List[Dict]: List of students with enrollment details
        """
        db = DatabaseConnection()
        students = []

        query = """
            SELECT s.student_id, s.first_name, s.last_name, s.email, e.enrollment_date, e.grade
            FROM enrollments e
            JOIN students s ON e.student_id = s.student_id
            WHERE e.course_id = %s
            ORDER BY s.student_id
        """
        results = db.fetch_all(query, (course_id,))

        for result in results:
            students.append({
                'student_id': result[0],
                'first_name': result[1],
                'last_name': result[2],
                'email': result[3],
                'enrollment_date': result[4],
                'grade': result[5]
            })
        return students

    @staticmethod
    def get_all_enrollments() -> List[Dict[str, Any]]:
        """Get all enrollments in the system.

        Returns:
            List[Dict]: List of all enrollments
        """
        db = DatabaseConnection()
        enrollments = []

        query = """
            SELECT e.enrollment_id, s.student_id, s.first_name, s.last_name,
                   c.course_id, c.course_name, e.enrollment_date, e.grade
            FROM enrollments e
            JOIN students s ON e.student_id = s.student_id
            JOIN courses c ON e.course_id = c.course_id
            ORDER BY e.enrollment_id
        """
        results = db.fetch_all(query)

        for result in results:
            enrollments.append({
                'enrollment_id': result[0],
                'student_id': result[1],
                'student_name': f"{result[2]} {result[3]}",
                'course_id': result[4],
                'course_name': result[5],
                'enrollment_date': result[6],
                'grade': result[7]
            })
        return enrollments

    @staticmethod
    def remove_enrollment(student_id: int, course_id: int) -> bool:
        """Remove a student's enrollment from a course.

        Args:
            student_id: ID of the student
            course_id: ID of the course

        Returns:
            bool: True if successful, False otherwise
        """
        db = DatabaseConnection()

        # Check if enrollment exists
        enrollment = db.fetch_one(
            "SELECT enrollment_id FROM enrollments WHERE student_id = %s AND course_id = %s",
            (student_id, course_id)
        )
        if not enrollment:
            print("✗ Enrollment record not found")
            return False

        # Delete enrollment
        if db.execute_query(
            "DELETE FROM enrollments WHERE student_id = %s AND course_id = %s",
            (student_id, course_id)
        ):
            print(f"✓ Student {student_id} removed from Course {course_id} successfully")
            return True
        else:
            print("✗ Failed to remove enrollment")
            return False

    @staticmethod
    def update_grade(student_id: int, course_id: int, grade: str) -> bool:
        """Update a student's grade in a course.

        Args:
            student_id: ID of the student
            course_id: ID of the course
            grade: Grade to assign (A, B+, B, C, etc.)

        Returns:
            bool: True if successful, False otherwise
        """
        db = DatabaseConnection()

        # Validate grade
        valid_grades = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D', 'F'}
        if grade not in valid_grades:
            print(f"✗ Invalid grade. Valid grades are: {', '.join(valid_grades)}")
            return False

        # Check if enrollment exists
        enrollment = db.fetch_one(
            "SELECT enrollment_id FROM enrollments WHERE student_id = %s AND course_id = %s",
            (student_id, course_id)
        )
        if not enrollment:
            print("✗ Enrollment record not found")
            return False

        # Update grade
        if db.execute_query(
            "UPDATE enrollments SET grade = %s WHERE student_id = %s AND course_id = %s",
            (grade, student_id, course_id)
        ):
            print(f"✓ Grade updated successfully for Student {student_id} in Course {course_id}")
            return True
        else:
            print("✗ Failed to update grade")
            return False
