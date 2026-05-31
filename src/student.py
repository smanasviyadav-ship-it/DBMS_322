"""Student Management Module

This module handles all student-related operations including add, update, delete, and search.
It implements OOP principles with proper validation and exception handling.
"""

from db_connection import DatabaseConnection
from datetime import datetime
from typing import List, Optional, Tuple, Dict, Any


class Student:
    """Class to manage student records in the database."""

    def __init__(self, first_name: str, last_name: str, email: str,
                 gender: str = None, date_of_birth: str = None, phone: str = None):
        """Initialize a Student object.

        Args:
            first_name: Student's first name
            last_name: Student's last name
            email: Student's email address (unique)
            gender: Student's gender
            date_of_birth: Student's date of birth (YYYY-MM-DD)
            phone: Student's phone number
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.phone = phone
        self.db = DatabaseConnection()

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format.

        Args:
            email: Email address to validate

        Returns:
            bool: True if valid, False otherwise
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

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

    def add_student(self) -> Optional[int]:
        """Add a new student to the database.

        Returns:
            int: Student ID if successful, None otherwise
        """
        # Validate inputs
        if not self.first_name or not self.last_name:
            print("✗ First name and last name are required")
            return None

        if not self.validate_email(self.email):
            print("✗ Invalid email format")
            return None

        if self.date_of_birth and not self.validate_date(self.date_of_birth):
            print("✗ Invalid date format. Use YYYY-MM-DD")
            return None

        # Check if email already exists
        existing = self.db.fetch_one(
            "SELECT student_id FROM students WHERE email = %s",
            (self.email,)
        )
        if existing:
            print("✗ Email already exists in the system")
            return None

        # Insert student
        query = """
            INSERT INTO students (first_name, last_name, gender, date_of_birth, email, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            self.first_name, self.last_name, self.gender,
            self.date_of_birth, self.email, self.phone
        )

        if self.db.execute_query(query, params):
            # Get the inserted student ID
            result = self.db.fetch_one(
                "SELECT student_id FROM students WHERE email = %s",
                (self.email,)
            )
            if result:
                print(f"✓ Student added successfully with ID: {result[0]}")
                return result[0]
        else:
            print("✗ Failed to add student")
            return None

    @staticmethod
    def get_student_by_id(student_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve student information by ID.

        Args:
            student_id: ID of the student to retrieve

        Returns:
            Dict: Student details or None if not found
        """
        db = DatabaseConnection()
        result = db.fetch_one(
            "SELECT * FROM students WHERE student_id = %s",
            (student_id,)
        )
        if result:
            return {
                'student_id': result[0],
                'first_name': result[1],
                'last_name': result[2],
                'gender': result[3],
                'date_of_birth': result[4],
                'email': result[5],
                'phone': result[6]
            }
        return None

    @staticmethod
    def search_students_by_name(first_name: str = None, last_name: str = None) -> List[Dict[str, Any]]:
        """Search students by name.

        Args:
            first_name: First name to search (partial match)
            last_name: Last name to search (partial match)

        Returns:
            List[Dict]: List of matching students
        """
        db = DatabaseConnection()
        students = []

        if first_name and last_name:
            query = "SELECT * FROM students WHERE first_name LIKE %s AND last_name LIKE %s"
            results = db.fetch_all(query, (f"%{first_name}%", f"%{last_name}%"))
        elif first_name:
            query = "SELECT * FROM students WHERE first_name LIKE %s"
            results = db.fetch_all(query, (f"%{first_name}%",))
        elif last_name:
            query = "SELECT * FROM students WHERE last_name LIKE %s"
            results = db.fetch_all(query, (f"%{last_name}%",))
        else:
            return students

        for result in results:
            students.append({
                'student_id': result[0],
                'first_name': result[1],
                'last_name': result[2],
                'gender': result[3],
                'date_of_birth': result[4],
                'email': result[5],
                'phone': result[6]
            })
        return students

    @staticmethod
    def get_all_students() -> List[Dict[str, Any]]:
        """Retrieve all students from the database.

        Returns:
            List[Dict]: List of all students
        """
        db = DatabaseConnection()
        results = db.fetch_all("SELECT * FROM students ORDER BY student_id")
        students = []

        for result in results:
            students.append({
                'student_id': result[0],
                'first_name': result[1],
                'last_name': result[2],
                'gender': result[3],
                'date_of_birth': result[4],
                'email': result[5],
                'phone': result[6]
            })
        return students

    @staticmethod
    def update_student(student_id: int, **kwargs) -> bool:
        """Update student information.

        Args:
            student_id: ID of student to update
            **kwargs: Fields to update (first_name, last_name, gender, date_of_birth, email, phone)

        Returns:
            bool: True if successful, False otherwise
        """
        db = DatabaseConnection()

        # Verify student exists
        if not db.fetch_one("SELECT student_id FROM students WHERE student_id = %s", (student_id,)):
            print("✗ Student not found")
            return False

        # Validate email if provided
        if 'email' in kwargs and not Student.validate_email(kwargs['email']):
            print("✗ Invalid email format")
            return False

        # Validate date if provided
        if 'date_of_birth' in kwargs and kwargs['date_of_birth'] and not Student.validate_date(kwargs['date_of_birth']):
            print("✗ Invalid date format. Use YYYY-MM-DD")
            return False

        # Build update query
        allowed_fields = {'first_name', 'last_name', 'gender', 'date_of_birth', 'email', 'phone'}
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields and v is not None}

        if not update_fields:
            print("✗ No valid fields to update")
            return False

        set_clause = ", ".join([f"{field} = %s" for field in update_fields.keys()])
        query = f"UPDATE students SET {set_clause} WHERE student_id = %s"
        params = tuple(update_fields.values()) + (student_id,)

        if db.execute_query(query, params):
            print(f"✓ Student ID {student_id} updated successfully")
            return True
        else:
            print("✗ Failed to update student")
            return False

    @staticmethod
    def delete_student(student_id: int) -> bool:
        """Delete a student from the database.

        Args:
            student_id: ID of student to delete

        Returns:
            bool: True if successful, False otherwise
        """
        db = DatabaseConnection()

        # Verify student exists
        student = db.fetch_one("SELECT * FROM students WHERE student_id = %s", (student_id,))
        if not student:
            print("✗ Student not found")
            return False

        # Delete student (cascading delete will remove enrollments)
        if db.execute_query("DELETE FROM students WHERE student_id = %s", (student_id,)):
            print(f"✓ Student ID {student_id} deleted successfully")
            return True
        else:
            print("✗ Failed to delete student")
            return False
