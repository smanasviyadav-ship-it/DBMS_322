"""Course Management Module

This module handles all course-related operations including
adding, updating, deleting, and retrieving courses.
"""

from db_connection import db


class Course:
    """Manages course operations in the database."""

    @staticmethod
    def validate_credits(credits):
        """Validate course credits.

        Args:
            credits (int): Number of credits

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            credits_int = int(credits)
            return credits_int > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def add_course(course_name, credits):
        """Add a new course to the database.

        Args:
            course_name (str): Name of the course
            credits (int): Number of credits

        Returns:
            dict: Result with 'success' and 'message' keys
        """
        # Validate inputs
        if not course_name or len(course_name.strip()) == 0:
            return {'success': False, 'message': 'Course name is required'}

        if not Course.validate_credits(credits):
            return {'success': False, 'message': 'Credits must be a positive integer'}

        # Check if course already exists
        query = "SELECT course_id FROM courses WHERE course_name = %s"
        existing = db.fetch_one(query, (course_name,))
        if existing:
            return {'success': False, 'message': 'Course already exists'}

        # Insert new course
        query = "INSERT INTO courses (course_name, credits) VALUES (%s, %s)"
        result = db.execute_query(query, (course_name, credits))
        if result is not None:
            return {'success': True, 'message': f'Course {course_name} added successfully'}
        else:
            return {'success': False, 'message': 'Error adding course'}

    @staticmethod
    def update_course(course_id, course_name=None, credits=None):
        """Update course information.

        Args:
            course_id (int): Course ID to update
            course_name (str): New course name
            credits (int): New credits value

        Returns:
            dict: Result with 'success' and 'message' keys
        """
        # Check if course exists
        query = "SELECT course_id FROM courses WHERE course_id = %s"
        course = db.fetch_one(query, (course_id,))
        if not course:
            return {'success': False, 'message': 'Course not found'}

        # Validate credits if being updated
        if credits is not None and not Course.validate_credits(credits):
            return {'success': False, 'message': 'Credits must be a positive integer'}

        # Check for duplicate course name
        if course_name:
            query = "SELECT course_id FROM courses WHERE course_name = %s AND course_id != %s"
            existing = db.fetch_one(query, (course_name, course_id))
            if existing:
                return {'success': False, 'message': 'Course name already exists'}

        # Build update query
        updates = []
        params = []
        if course_name:
            updates.append("course_name = %s")
            params.append(course_name)
        if credits is not None:
            updates.append("credits = %s")
            params.append(credits)

        if not updates:
            return {'success': False, 'message': 'No fields to update'}

        params.append(course_id)
        query = f"UPDATE courses SET {', '.join(updates)} WHERE course_id = %s"
        result = db.execute_query(query, tuple(params))
        if result is not None and result > 0:
            return {'success': True, 'message': 'Course updated successfully'}
        else:
            return {'success': False, 'message': 'Error updating course'}

    @staticmethod
    def delete_course(course_id):
        """Delete a course from the database.

        Args:
            course_id (int): Course ID to delete

        Returns:
            dict: Result with 'success' and 'message' keys
        """
        # Check if course exists
        query = "SELECT course_name FROM courses WHERE course_id = %s"
        course = db.fetch_one(query, (course_id,))
        if not course:
            return {'success': False, 'message': 'Course not found'}

        # Delete course (CASCADE will handle enrollments)
        query = "DELETE FROM courses WHERE course_id = %s"
        result = db.execute_query(query, (course_id,))
        if result is not None and result > 0:
            return {'success': True, 'message': f'Course {course["course_name"]} deleted successfully'}
        else:
            return {'success': False, 'message': 'Error deleting course'}

    @staticmethod
    def search_course(course_id=None, course_name=None):
        """Search for courses by various criteria.

        Args:
            course_id (int): Course ID to search
            course_name (str): Course name to search (partial match)

        Returns:
            list: List of matching courses
        """
        query = "SELECT * FROM courses WHERE 1=1"
        params = []

        if course_id:
            query += " AND course_id = %s"
            params.append(course_id)
        if course_name:
            query += " AND course_name LIKE %s"
            params.append(f"%{course_name}%")

        if params:
            results = db.fetch_all(query, tuple(params))
        else:
            results = db.fetch_all(query)
        return results

    @staticmethod
    def get_all_courses():
        """Retrieve all courses from the database.

        Returns:
            list: All courses in the database
        """
        query = "SELECT * FROM courses ORDER BY course_name"
        return db.fetch_all(query)

    @staticmethod
    def get_course_by_id(course_id):
        """Retrieve a specific course by ID.

        Args:
            course_id (int): Course ID

        Returns:
            dict: Course information or None if not found
        """
        query = "SELECT * FROM courses WHERE course_id = %s"
        return db.fetch_one(query, (course_id,))
