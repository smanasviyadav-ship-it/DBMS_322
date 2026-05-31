"""Enrollment Management Module

This module handles all enrollment-related operations including
enrolling students in courses, removing enrollments, and viewing enrollments.
"""

from db_connection import db
from datetime import datetime
from student import Student
from course import Course


class Enrollment:
    """Manages enrollment operations in the database."""

    @staticmethod
    def validate_date(date_str):
        """Validate date format (YYYY-MM-DD).

        Args:
            date_str (str): Date string to validate

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    @staticmethod
    def enroll_student(student_id, course_id, enrollment_date=None):
        """Enroll a student in a course.

        Args:
            student_id (int): Student ID
            course_id (int): Course ID
            enrollment_date (str): Enrollment date (YYYY-MM-DD), defaults to today

        Returns:
            dict: Result with 'success' and 'message' keys
        """
        # Validate student exists
        student = Student.get_student_by_id(student_id)
        if not student:
            return {'success': False, 'message': 'Student not found'}

        # Validate course exists
        course = Course.get_course_by_id(course_id)
        if not course:
            return {'success': False, 'message': 'Course not found'}

        # Set enrollment date to today if not provided
        if enrollment_date is None:
            enrollment_date = datetime.now().strftime('%Y-%m-%d')
        else:
            if not Enrollment.validate_date(enrollment_date):
                return {'success': False, 'message': 'Invalid date format. Use YYYY-MM-DD'}

        # Check if student is already enrolled
        query = "SELECT enrollment_id FROM enrollments WHERE student_id = %s AND course_id = %s"
        existing = db.fetch_one(query, (student_id, course_id))
        if existing:
            return {'success': False, 'message': 'Student is already enrolled in this course'}

        # Insert enrollment
        query = """
            INSERT INTO enrollments (student_id, course_id, enrollment_date)
            VALUES (%s, %s, %s)
        """
        result = db.execute_query(query, (student_id, course_id, enrollment_date))
        if result is not None:
            return {'success': True, 'message': f'Student {student["first_name"]} {student["last_name"]} enrolled in {course["course_name"]}'}
        else:
            return {'success': False, 'message': 'Error enrolling student'}

    @staticmethod
    def remove_enrollment(enrollment_id):
        """Remove an enrollment.

        Args:
            enrollment_id (int): Enrollment ID to remove

        Returns:
            dict: Result with 'success' and 'message' keys
        """
        # Check if enrollment exists
        query = "SELECT enrollment_id FROM enrollments WHERE enrollment_id = %s"
        enrollment = db.fetch_one(query, (enrollment_id,))
        if not enrollment:
            return {'success': False, 'message': 'Enrollment not found'}

        # Delete enrollment
        query = "DELETE FROM enrollments WHERE enrollment_id = %s"
        result = db.execute_query(query, (enrollment_id,))
        if result is not None and result > 0:
            return {'success': True, 'message': 'Enrollment removed successfully'}
        else:
            return {'success': False, 'message': 'Error removing enrollment'}

    @staticmethod
    def remove_enrollment_by_student_course(student_id, course_id):
        """Remove enrollment for a specific student-course combination.

        Args:
            student_id (int): Student ID
            course_id (int): Course ID

        Returns:
            dict: Result with 'success' and 'message' keys
        """
        query = "DELETE FROM enrollments WHERE student_id = %s AND course_id = %s"
        result = db.execute_query(query, (student_id, course_id))
        if result is not None and result > 0:
            return {'success': True, 'message': 'Enrollment removed successfully'}
        else:
            return {'success': False, 'message': 'Enrollment not found or error removing it'}

    @staticmethod
    def get_all_enrollments():
        """Retrieve all enrollments with student and course details.

        Returns:
            list: All enrollments with joined data
        """
        query = """
            SELECT e.enrollment_id, e.student_id, e.course_id, e.enrollment_date,
                   s.first_name, s.last_name, s.email,
                   c.course_name, c.credits
            FROM enrollments e
            JOIN students s ON e.student_id = s.student_id
            JOIN courses c ON e.course_id = c.course_id
            ORDER BY s.first_name, s.last_name, c.course_name
        """
        return db.fetch_all(query)

    @staticmethod
    def get_enrollments_by_student(student_id):
        """Get all enrollments for a specific student.

        Args:
            student_id (int): Student ID

        Returns:
            list: Enrollments for the student
        """
        query = """
            SELECT e.enrollment_id, e.student_id, e.course_id, e.enrollment_date,
                   c.course_name, c.credits
            FROM enrollments e
            JOIN courses c ON e.course_id = c.course_id
            WHERE e.student_id = %s
            ORDER BY c.course_name
        """
        return db.fetch_all(query, (student_id,))

    @staticmethod
    def get_enrollments_by_course(course_id):
        """Get all students enrolled in a specific course.

        Args:
            course_id (int): Course ID

        Returns:
            list: Students enrolled in the course
        """
        query = """
            SELECT e.enrollment_id, e.student_id, e.course_id, e.enrollment_date,
                   s.first_name, s.last_name, s.email
            FROM enrollments e
            JOIN students s ON e.student_id = s.student_id
            WHERE e.course_id = %s
            ORDER BY s.first_name, s.last_name
        """
        return db.fetch_all(query, (course_id,))

    @staticmethod
    def get_enrollment_by_id(enrollment_id):
        """Retrieve a specific enrollment.

        Args:
            enrollment_id (int): Enrollment ID

        Returns:
            dict: Enrollment information or None if not found
        """
        query = """
            SELECT e.enrollment_id, e.student_id, e.course_id, e.enrollment_date,
                   s.first_name, s.last_name, c.course_name
            FROM enrollments e
            JOIN students s ON e.student_id = s.student_id
            JOIN courses c ON e.course_id = c.course_id
            WHERE e.enrollment_id = %s
        """
        return db.fetch_one(query, (enrollment_id,))
