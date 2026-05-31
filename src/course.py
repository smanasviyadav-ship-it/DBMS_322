"""Course Management Module

This module handles all course-related operations including add, update, delete, and retrieve.
It implements OOP principles with proper validation and exception handling.
"""

from db_connection import DatabaseConnection
from typing import List, Optional, Dict, Any


class Course:
    """Class to manage course records in the database."""

    def __init__(self, course_name: str, credits: int, description: str = None):
        """Initialize a Course object.

        Args:
            course_name: Name of the course
            credits: Number of credits for the course
            description: Course description
        """
        self.course_name = course_name
        self.credits = credits
        self.description = description
        self.db = DatabaseConnection()

    @staticmethod
    def validate_credits(credits: int) -> bool:
        """Validate credits value.

        Args:
            credits: Number of credits to validate

        Returns:
            bool: True if valid, False otherwise
        """
        return isinstance(credits, int) and 1 <= credits <= 10

    def add_course(self) -> Optional[int]:
        """Add a new course to the database.

        Returns:
            int: Course ID if successful, None otherwise
        """
        # Validate inputs
        if not self.course_name or len(self.course_name.strip()) == 0:
            print("✗ Course name is required")
            return None

        if not self.validate_credits(self.credits):
            print("✗ Credits must be between 1 and 10")
            return None

        # Check if course already exists
        existing = self.db.fetch_one(
            "SELECT course_id FROM courses WHERE course_name = %s",
            (self.course_name,)
        )
        if existing:
            print("✗ Course with this name already exists")
            return None

        # Insert course
        query = """
            INSERT INTO courses (course_name, credits, description)
            VALUES (%s, %s, %s)
        """
        params = (self.course_name, self.credits, self.description)

        if self.db.execute_query(query, params):
            # Get the inserted course ID
            result = self.db.fetch_one(
                "SELECT course_id FROM courses WHERE course_name = %s",
                (self.course_name,)
            )
            if result:
                print(f"✓ Course added successfully with ID: {result[0]}")
                return result[0]
        else:
            print("✗ Failed to add course")
            return None

    @staticmethod
    def get_course_by_id(course_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve course information by ID.

        Args:
            course_id: ID of the course to retrieve

        Returns:
            Dict: Course details or None if not found
        """
        db = DatabaseConnection()
        result = db.fetch_one(
            "SELECT * FROM courses WHERE course_id = %s",
            (course_id,)
        )
        if result:
            return {
                'course_id': result[0],
                'course_name': result[1],
                'credits': result[2],
                'description': result[3] if len(result) > 3 else None
            }
        return None

    @staticmethod
    def search_courses_by_name(course_name: str) -> List[Dict[str, Any]]:
        """Search courses by name.

        Args:
            course_name: Course name to search (partial match)

        Returns:
            List[Dict]: List of matching courses
        """
        db = DatabaseConnection()
        courses = []
        results = db.fetch_all(
            "SELECT * FROM courses WHERE course_name LIKE %s ORDER BY course_id",
            (f"%{course_name}%",)
        )

        for result in results:
            courses.append({
                'course_id': result[0],
                'course_name': result[1],
                'credits': result[2],
                'description': result[3] if len(result) > 3 else None
            })
        return courses

    @staticmethod
    def get_all_courses() -> List[Dict[str, Any]]:
        """Retrieve all courses from the database.

        Returns:
            List[Dict]: List of all courses
        """
        db = DatabaseConnection()
        results = db.fetch_all("SELECT * FROM courses ORDER BY course_id")
        courses = []

        for result in results:
            courses.append({
                'course_id': result[0],
                'course_name': result[1],
                'credits': result[2],
                'description': result[3] if len(result) > 3 else None
            })
        return courses

    @staticmethod
    def update_course(course_id: int, **kwargs) -> bool:
        """Update course information.

        Args:
            course_id: ID of course to update
            **kwargs: Fields to update (course_name, credits, description)

        Returns:
            bool: True if successful, False otherwise
        """
        db = DatabaseConnection()

        # Verify course exists
        if not db.fetch_one("SELECT course_id FROM courses WHERE course_id = %s", (course_id,)):
            print("✗ Course not found")
            return False

        # Validate credits if provided
        if 'credits' in kwargs and not Course.validate_credits(kwargs['credits']):
            print("✗ Credits must be between 1 and 10")
            return False

        # Build update query
        allowed_fields = {'course_name', 'credits', 'description'}
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields and v is not None}

        if not update_fields:
            print("✗ No valid fields to update")
            return False

        set_clause = ", ".join([f"{field} = %s" for field in update_fields.keys()])
        query = f"UPDATE courses SET {set_clause} WHERE course_id = %s"
        params = tuple(update_fields.values()) + (course_id,)

        if db.execute_query(query, params):
            print(f"✓ Course ID {course_id} updated successfully")
            return True
        else:
            print("✗ Failed to update course")
            return False

    @staticmethod
    def delete_course(course_id: int) -> bool:
        """Delete a course from the database.

        Args:
            course_id: ID of course to delete

        Returns:
            bool: True if successful, False otherwise
        """
        db = DatabaseConnection()

        # Verify course exists
        if not db.fetch_one("SELECT course_id FROM courses WHERE course_id = %s", (course_id,)):
            print("✗ Course not found")
            return False

        # Delete course (cascading delete will remove enrollments)
        if db.execute_query("DELETE FROM courses WHERE course_id = %s", (course_id,)):
            print(f"✓ Course ID {course_id} deleted successfully")
            return True
        else:
            print("✗ Failed to delete course")
            return False
