"""Reports Module

This module generates various reports about students, courses, and enrollments.
"""

from db_connection import db


class Reports:
    """Generates reports from the database."""

    @staticmethod
    def get_total_students():
        """Get total number of students.

        Returns:
            int: Total number of students
        """
        query = "SELECT COUNT(*) as total FROM students"
        result = db.fetch_one(query)
        return result['total'] if result else 0

    @staticmethod
    def get_total_courses():
        """Get total number of courses.

        Returns:
            int: Total number of courses
        """
        query = "SELECT COUNT(*) as total FROM courses"
        result = db.fetch_one(query)
        return result['total'] if result else 0

    @staticmethod
    def get_total_enrollments():
        """Get total number of enrollments.

        Returns:
            int: Total number of enrollments
        """
        query = "SELECT COUNT(*) as total FROM enrollments"
        result = db.fetch_one(query)
        return result['total'] if result else 0

    @staticmethod
    def get_student_enrollment_report():
        """Generate a report of all students with their course enrollments.

        Returns:
            list: Report data with student and enrollment information
        """
        query = """
            SELECT 
                s.student_id,
                s.first_name,
                s.last_name,
                s.email,
                s.phone,
                COUNT(e.enrollment_id) as enrolled_courses,
                GROUP_CONCAT(c.course_name SEPARATOR ', ') as courses
            FROM students s
            LEFT JOIN enrollments e ON s.student_id = e.student_id
            LEFT JOIN courses c ON e.course_id = c.course_id
            GROUP BY s.student_id, s.first_name, s.last_name, s.email, s.phone
            ORDER BY s.first_name, s.last_name
        """
        return db.fetch_all(query)

    @staticmethod
    def get_course_enrollment_report():
        """Generate a report of all courses with their enrolled students.

        Returns:
            list: Report data with course and enrollment information
        """
        query = """
            SELECT 
                c.course_id,
                c.course_name,
                c.credits,
                COUNT(e.enrollment_id) as total_students,
                GROUP_CONCAT(CONCAT(s.first_name, ' ', s.last_name) SEPARATOR ', ') as students
            FROM courses c
            LEFT JOIN enrollments e ON c.course_id = e.course_id
            LEFT JOIN students s ON e.student_id = s.student_id
            GROUP BY c.course_id, c.course_name, c.credits
            ORDER BY c.course_name
        """
        return db.fetch_all(query)

    @staticmethod
    def get_enrollment_statistics():
        """Get enrollment statistics.

        Returns:
            dict: Statistics including average courses per student, etc.
        """
        query = """
            SELECT 
                COUNT(DISTINCT s.student_id) as total_students,
                COUNT(DISTINCT c.course_id) as total_courses,
                COUNT(e.enrollment_id) as total_enrollments,
                AVG(course_count.count) as avg_courses_per_student,
                MAX(course_count.count) as max_courses_per_student,
                MIN(course_count.count) as min_courses_per_student
            FROM students s
            LEFT JOIN enrollments e ON s.student_id = e.student_id
            LEFT JOIN courses c ON e.course_id = c.course_id
            LEFT JOIN (
                SELECT student_id, COUNT(*) as count
                FROM enrollments
                GROUP BY student_id
            ) course_count ON s.student_id = course_count.student_id
        """
        return db.fetch_one(query)

    @staticmethod
    def get_students_by_course(course_id):
        """Get detailed report of students in a specific course.

        Args:
            course_id (int): Course ID

        Returns:
            list: Students enrolled in the course
        """
        query = """
            SELECT 
                s.student_id,
                s.first_name,
                s.last_name,
                s.email,
                s.phone,
                e.enrollment_date
            FROM students s
            JOIN enrollments e ON s.student_id = e.student_id
            WHERE e.course_id = %s
            ORDER BY s.first_name, s.last_name
        """
        return db.fetch_all(query, (course_id,))

    @staticmethod
    def get_courses_by_student(student_id):
        """Get detailed report of courses for a specific student.

        Args:
            student_id (int): Student ID

        Returns:
            list: Courses the student is enrolled in
        """
        query = """
            SELECT 
                c.course_id,
                c.course_name,
                c.credits,
                e.enrollment_date
            FROM courses c
            JOIN enrollments e ON c.course_id = e.course_id
            WHERE e.student_id = %s
            ORDER BY c.course_name
        """
        return db.fetch_all(query, (student_id,))

    @staticmethod
    def get_total_credits_by_student():
        """Get total credits enrolled for each student.

        Returns:
            list: Students with their total credits
        """
        query = """
            SELECT 
                s.student_id,
                s.first_name,
                s.last_name,
                SUM(c.credits) as total_credits,
                COUNT(e.enrollment_id) as total_courses
            FROM students s
            LEFT JOIN enrollments e ON s.student_id = e.student_id
            LEFT JOIN courses c ON e.course_id = c.course_id
            GROUP BY s.student_id, s.first_name, s.last_name
            ORDER BY total_credits DESC, s.first_name
        """
        return db.fetch_all(query)

    @staticmethod
    def print_summary_report():
        """Print a comprehensive summary report."""
        print("\n" + "="*60)
        print("STUDENT MANAGEMENT SYSTEM - SUMMARY REPORT")
        print("="*60)

        total_students = Reports.get_total_students()
        total_courses = Reports.get_total_courses()
        total_enrollments = Reports.get_total_enrollments()

        print(f"\nTotal Students: {total_students}")
        print(f"Total Courses: {total_courses}")
        print(f"Total Enrollments: {total_enrollments}")

        if total_students > 0 and total_enrollments > 0:
            avg_enrollments = total_enrollments / total_students
            print(f"Average Enrollments per Student: {avg_enrollments:.2f}")

        stats = Reports.get_enrollment_statistics()
        if stats:
            print(f"\nAverage Courses per Student: {stats.get('avg_courses_per_student', 0) or 0:.2f}")
            print(f"Max Courses per Student: {stats.get('max_courses_per_student', 0) or 0}")
            print(f"Min Courses per Student: {stats.get('min_courses_per_student', 0) or 0}")

        print("\n" + "="*60 + "\n")
