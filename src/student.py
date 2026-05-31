"""Student Management Module

This module handles all student-related operations including
adding, updating, deleting, and searching for students.
"""

from db_connection import db
import re
from datetime import datetime


class Student:
    """Manages student operations in the database."""

    @staticmethod
    def validate_email(email):
        """Validate email format.

        Args:
            email (str): Email address to validate

        Returns:
            bool: True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_phone(phone):
        """Validate phone number format.

        Args:
            phone (str): Phone number to validate

        Returns:
            bool: True if valid, False otherwise
        """
        pattern = r'^[0-9\-\+\(\)\s]+$'
        return len(phone) >= 7 and re.match(pattern, phone) is not None

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
    def add_student(first_name, last_name, gender, date_of_birth, email, phone):
        """Add a new student to the database.

        Args:
            first_name (str): Student's first name
            last_name (str): Student's last name
            gender (str): Student's gender
            date_of_birth (str): Date of birth (YYYY-MM-DD)
            email (str): Student's email
            phone (str): Student's phone number

        Returns:
            dict: Result with 'success' and 'message' keys
        """
        # Validate inputs
        if not first_name or not last_name:
            return {'success': False, 'message': 'First name and last name are required'}

        if not Student.validate_email(email):
            return {'success': False, 'message': 'Invalid email format'}

        if not Student.validate_phone(phone):
            return {'success': False, 'message': 'Invalid phone number format'}

        if not Student.validate_date(date_of_birth):
            return {'success': False, 'message': 'Invalid date format. Use YYYY-MM-DD'}

        # Check if email already exists
        query = "SELECT student_id FROM students WHERE email = %s"
        existing = db.fetch_one(query, (email,))
        if existing:
            return {'success': False, 'message': 'Email already exists'}

        # Insert new student
        query = """
            INSERT INTO students (first_name, last_name, gender, date_of_birth, email, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        result = db.execute_query(query, (first_name, last_name, gender, date_of_birth, email, phone))
        if result is not None:
            return {'success': True, 'message': f'Student {first_name} {last_name} added successfully'}
        else:
            return {'success': False, 'message': 'Error adding student'}

    @staticmethod
    def update_student(student_id, **kwargs):
        """Update student information.

        Args:
            student_id (int): Student ID to update
            **kwargs: Fields to update (first_name, last_name, gender, etc.)

        Returns:
            dict: Result with 'success' and 'message' keys
        """
        # Check if student exists
        query = "SELECT student_id FROM students WHERE student_id = %s"
        student = db.fetch_one(query, (student_id,))
        if not student:
            return {'success': False, 'message': 'Student not found'}

        # Validate email if being updated
        if 'email' in kwargs and not Student.validate_email(kwargs['email']):
            return {'success': False, 'message': 'Invalid email format'}

        # Validate phone if being updated
        if 'phone' in kwargs and not Student.validate_phone(kwargs['phone']):
            return {'success': False, 'message': 'Invalid phone number format'}

        # Validate date if being updated
        if 'date_of_birth' in kwargs and not Student.validate_date(kwargs['date_of_birth']):
            return {'success': False, 'message': 'Invalid date format. Use YYYY-MM-DD'}

        # Check for duplicate email
        if 'email' in kwargs:
            query = "SELECT student_id FROM students WHERE email = %s AND student_id != %s"
            existing = db.fetch_one(query, (kwargs['email'], student_id))
            if existing:
                return {'success': False, 'message': 'Email already exists'}

        # Build update query
        allowed_fields = {'first_name', 'last_name', 'gender', 'date_of_birth', 'email', 'phone'}
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}

        if not update_fields:
            return {'success': False, 'message': 'No valid fields to update'}

        set_clause = ', '.join([f"{field} = %s" for field in update_fields.keys()])
        values = list(update_fields.values()) + [student_id]

        query = f"UPDATE students SET {set_clause} WHERE student_id = %s"
        result = db.execute_query(query, tuple(values))
        if result is not None and result > 0:
            return {'success': True, 'message': 'Student updated successfully'}
        else:
            return {'success': False, 'message': 'Error updating student'}

    @staticmethod
    def delete_student(student_id):
        """Delete a student from the database.

        Args:
            student_id (int): Student ID to delete

        Returns:
            dict: Result with 'success' and 'message' keys
        """
        # Check if student exists
        query = "SELECT first_name, last_name FROM students WHERE student_id = %s"
        student = db.fetch_one(query, (student_id,))
        if not student:
            return {'success': False, 'message': 'Student not found'}

        # Delete student (CASCADE will handle enrollments)
        query = "DELETE FROM students WHERE student_id = %s"
        result = db.execute_query(query, (student_id,))
        if result is not None and result > 0:
            return {'success': True, 'message': f'Student {student["first_name"]} {student["last_name"]} deleted successfully'}
        else:
            return {'success': False, 'message': 'Error deleting student'}

    @staticmethod
    def search_student(student_id=None, email=None, first_name=None, last_name=None):
        """Search for students by various criteria.

        Args:
            student_id (int): Student ID to search
            email (str): Email to search
            first_name (str): First name to search
            last_name (str): Last name to search

        Returns:
            list: List of matching students
        """
        query = "SELECT * FROM students WHERE 1=1"
        params = []

        if student_id:
            query += " AND student_id = %s"
            params.append(student_id)
        if email:
            query += " AND email LIKE %s"
            params.append(f"%{email}%")
        if first_name:
            query += " AND first_name LIKE %s"
            params.append(f"%{first_name}%")
        if last_name:
            query += " AND last_name LIKE %s"
            params.append(f"%{last_name}%")

        if params:
            results = db.fetch_all(query, tuple(params))
        else:
            results = db.fetch_all(query)
        return results

    @staticmethod
    def get_all_students():
        """Retrieve all students from the database.

        Returns:
            list: All students in the database
        """
        query = "SELECT * FROM students ORDER BY first_name, last_name"
        return db.fetch_all(query)

    @staticmethod
    def get_student_by_id(student_id):
        """Retrieve a specific student by ID.

        Args:
            student_id (int): Student ID

        Returns:
            dict: Student information or None if not found
        """
        query = "SELECT * FROM students WHERE student_id = %s"
        return db.fetch_one(query, (student_id,))
