"""Database Connection Module

This module handles the MySQL database connection and provides utilities
for executing queries with proper error handling and parameterized statements.
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DatabaseConnection:
    """Manages MySQL database connections and operations."""

    def __init__(self):
        """Initialize database connection parameters from environment variables."""
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'student_management_system')
        self.port = int(os.getenv('DB_PORT', 3306))
        self.connection = None

    def connect(self):
        """Establish a connection to the MySQL database.

        Returns:
            bool: True if connection successful, False otherwise.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            if self.connection.is_connected():
                print(f"Connected to MySQL database: {self.database}")
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False

    def disconnect(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Disconnected from MySQL database")

    def execute_query(self, query, params=None, fetch=False):
        """Execute a SQL query with optional parameters.

        Args:
            query (str): SQL query to execute
            params (tuple): Query parameters for parameterized queries
            fetch (bool): If True, fetch and return results

        Returns:
            list/int: Query results if fetch=True, affected rows if fetch=False
        """
        if not self.connection or not self.connection.is_connected():
            print("Database connection not established")
            return None

        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if fetch:
                results = cursor.fetchall()
                cursor.close()
                return results
            else:
                self.connection.commit()
                affected_rows = cursor.rowcount
                cursor.close()
                return affected_rows
        except Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            return None

    def execute_many(self, query, data):
        """Execute multiple queries with different parameters.

        Args:
            query (str): SQL query to execute
            data (list): List of parameter tuples

        Returns:
            bool: True if successful, False otherwise
        """
        if not self.connection or not self.connection.is_connected():
            print("Database connection not established")
            return False

        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, data)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error executing batch queries: {e}")
            self.connection.rollback()
            return False

    def fetch_one(self, query, params=None):
        """Fetch a single row from database.

        Args:
            query (str): SQL query to execute
            params (tuple): Query parameters

        Returns:
            dict: Single row as dictionary or None
        """
        if not self.connection or not self.connection.is_connected():
            print("Database connection not established")
            return None

        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            return None

    def fetch_all(self, query, params=None):
        """Fetch all rows from database.

        Args:
            query (str): SQL query to execute
            params (tuple): Query parameters

        Returns:
            list: All rows as list of dictionaries
        """
        if not self.connection or not self.connection.is_connected():
            print("Database connection not established")
            return []

        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"Error fetching data: {e}")
            return []


# Global database instance
db = DatabaseConnection()
