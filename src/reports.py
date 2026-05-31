"""Reports Module

This module provides reporting and analytics functionality for the Student Management System.
It generates various reports including enrollment summaries and statistics.
"""

from db_connection import DatabaseConnection
from typing import List, Dict, Any, Tuple
from datetime import datetime


class Reports:
    """Class to generate reports and analytics."""

    def __init__(self):
        """Initialize Reports object."""
        self.db = DatabaseConnection()

    def get_total_students(self) -> int:
        """Get total number of students in the system.

        Returns:
            int: Total number of students
        """
        result = self.db.fetch_one("SELECT COUNT(*) FROM students")
        return result[0] if result else 0

    def get_total_courses(self) -> int:
        """Get total number of courses in the system.

        Returns:
            int: Total number of courses
        """
        result = self.db.fetch_one("SELECT COUNT(*) FROM courses")
        return result[0] if result else 0

    def get_total_enrollments(self) -> int:
        """Get total number of enrollments in the system.

        Returns:
            int: Total number of enrollments
        """
        result = self.db.fetch_one("SELECT COUNT(*) FROM enrollments")
        return result[0] if result else 0

    def get_system_statistics(self) -> Dict[str, Any]:
        """Get overall system statistics.

        Returns:
            Dict: System statistics including counts and averages
        """
        total_students = self.get_total_students()
        total_courses = self.get_total_courses()
        total_enrollments = self.get_total_enrollments()

        avg_enrollments_per_student = (
            total_enrollments / total_students if total_students > 0 else 0
        )
        avg_students_per_course = (
            total_enrollments / total_courses if total_courses > 0 else 0
        )

        return {
            'total_students': total_students,
            'total_courses': total_courses,
            'total_enrollments': total_enrollments,
            'avg_enrollments_per_student': round(avg_enrollments_per_student, 2),
            'avg_students_per_course': round(avg_students_per_course, 2)
        }

    def get_student_enrollment_report(self) -> List[Dict[str, Any]]:
        """Get detailed enrollment report for each student.

        Returns:
            List[Dict]: Student enrollment information
        """
        query = """
            SELECT
                s.student_id,
                CONCAT(s.first_name, ' ', s.last_name) AS student_name,
                s.email,
                COUNT(e.enrollment_id) AS total_courses,
                GROUP_CONCAT(c.course_name SEPARATOR ', ') AS courses_enrolled,
                GROUP_CONCAT(e.grade SEPARATOR ', ') AS grades
            FROM students s
            LEFT JOIN enrollments e ON s.student_id = e.student_id
            LEFT JOIN courses c ON e.course_id = c.course_id
            GROUP BY s.student_id, s.first_name, s.last_name, s.email
            ORDER BY s.student_id
        """
        results = self.db.fetch_all(query)
        report = []

        for result in results:
            report.append({
                'student_id': result[0],
                'student_name': result[1],
                'email': result[2],
                'total_courses': result[3],
                'courses_enrolled': result[4] if result[4] else 'None',
                'grades': result[5] if result[5] else 'N/A'
            })
        return report

    def get_course_enrollment_report(self) -> List[Dict[str, Any]]:
        """Get detailed enrollment report for each course.

        Returns:
            List[Dict]: Course enrollment information
        """
        query = """
            SELECT
                c.course_id,
                c.course_name,
                c.credits,
                COUNT(e.enrollment_id) AS total_students,
                GROUP_CONCAT(CONCAT(s.first_name, ' ', s.last_name) SEPARATOR ', ') AS enrolled_students
            FROM courses c
            LEFT JOIN enrollments e ON c.course_id = e.course_id
            LEFT JOIN students s ON e.student_id = s.student_id
            GROUP BY c.course_id, c.course_name, c.credits
            ORDER BY c.course_id
        """
        results = self.db.fetch_all(query)
        report = []

        for result in results:
            report.append({
                'course_id': result[0],
                'course_name': result[1],
                'credits': result[2],
                'total_students': result[3],
                'enrolled_students': result[4] if result[4] else 'None'
            })
        return report

    def get_enrollment_by_date_range(self, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Get enrollments within a specific date range.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            List[Dict]: Enrollments within the date range
        """
        query = """
            SELECT
                e.enrollment_id,
                CONCAT(s.first_name, ' ', s.last_name) AS student_name,
                c.course_name,
                e.enrollment_date,
                e.grade
            FROM enrollments e
            JOIN students s ON e.student_id = s.student_id
            JOIN courses c ON e.course_id = c.course_id
            WHERE e.enrollment_date BETWEEN %s AND %s
            ORDER BY e.enrollment_date DESC
        """
        results = self.db.fetch_all(query, (start_date, end_date))
        report = []

        for result in results:
            report.append({
                'enrollment_id': result[0],
                'student_name': result[1],
                'course_name': result[2],
                'enrollment_date': result[3],
                'grade': result[4] if result[4] else 'Not Graded'
            })
        return report

    def get_top_enrolled_courses(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get the most enrolled courses.

        Args:
            limit: Maximum number of courses to return

        Returns:
            List[Dict]: Top enrolled courses
        """
        query = """
            SELECT
                c.course_id,
                c.course_name,
                c.credits,
                COUNT(e.enrollment_id) AS enrollment_count
            FROM courses c
            LEFT JOIN enrollments e ON c.course_id = e.course_id
            GROUP BY c.course_id, c.course_name, c.credits
            ORDER BY enrollment_count DESC
            LIMIT %s
        """
        results = self.db.fetch_all(query, (limit,))
        report = []

        for result in results:
            report.append({
                'course_id': result[0],
                'course_name': result[1],
                'credits': result[2],
                'enrollment_count': result[3]
            })
        return report

    def get_grade_distribution(self, course_id: int = None) -> Dict[str, int]:
        """Get grade distribution for all courses or a specific course.

        Args:
            course_id: Optional course ID to filter by

        Returns:
            Dict: Grade distribution counts
        """
        if course_id:
            query = "SELECT grade, COUNT(*) FROM enrollments WHERE course_id = %s AND grade IS NOT NULL GROUP BY grade"
            results = self.db.fetch_all(query, (course_id,))
        else:
            query = "SELECT grade, COUNT(*) FROM enrollments WHERE grade IS NOT NULL GROUP BY grade"
            results = self.db.fetch_all(query)

        distribution = {}
        for result in results:
            grade = result[0] if result[0] else 'Not Graded'
            count = result[1]
            distribution[grade] = count

        return distribution

    def export_report_to_text(self, report_type: str) -> str:
        """Generate a text representation of a report.

        Args:
            report_type: Type of report ('system', 'student_enrollment', 'course_enrollment')

        Returns:
            str: Formatted report text
        """
        report_text = f"\n{'='*80}\n"
        report_text += f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report_text += f"{'='*80}\n\n"

        if report_type == 'system':
            stats = self.get_system_statistics()
            report_text += "SYSTEM STATISTICS\n"
            report_text += "-" * 80 + "\n"
            report_text += f"Total Students: {stats['total_students']}\n"
            report_text += f"Total Courses: {stats['total_courses']}\n"
            report_text += f"Total Enrollments: {stats['total_enrollments']}\n"
            report_text += f"Average Courses per Student: {stats['avg_enrollments_per_student']}\n"
            report_text += f"Average Students per Course: {stats['avg_students_per_course']}\n"

        elif report_type == 'student_enrollment':
            enrollments = self.get_student_enrollment_report()
            report_text += "STUDENT ENROLLMENT REPORT\n"
            report_text += "-" * 80 + "\n"
            report_text += f"{'ID':<5} {'Name':<25} {'Email':<30} {'Courses':<10}\n"
            report_text += "-" * 80 + "\n"
            for enrollment in enrollments:
                report_text += f"{enrollment['student_id']:<5} {enrollment['student_name']:<25} {enrollment['email']:<30} {enrollment['total_courses']:<10}\n"

        elif report_type == 'course_enrollment':
            enrollments = self.get_course_enrollment_report()
            report_text += "COURSE ENROLLMENT REPORT\n"
            report_text += "-" * 80 + "\n"
            report_text += f"{'ID':<5} {'Course Name':<40} {'Credits':<8} {'Students':<10}\n"
            report_text += "-" * 80 + "\n"
            for enrollment in enrollments:
                report_text += f"{enrollment['course_id']:<5} {enrollment['course_name']:<40} {enrollment['credits']:<8} {enrollment['total_students']:<10}\n"

        report_text += f"\n{'='*80}\n"
        return report_text
