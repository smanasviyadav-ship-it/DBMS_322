"""Database Connection Module

This module handles all database connections and operations for the Student Management System.
It provides a singleton connection manager to ensure efficient database resource usage.
"""

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from typing import Optional, List, Tuple, Any

# Load environment variables from .env file
load_dotenv()


class DatabaseConnection:
    """Manages MySQL database connections and queries."""

    _instance: Optional['DatabaseConnection'] = None
    _connection = None

    def __new__(cls):
        """Implement singleton pattern for database connection."""
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize database connection with credentials from environment variables."""
        if self._connection is None:
            self.connect()

    def connect(self) -> bool:
        """Establish database connection using environment variables.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self._connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=int(os.getenv('DB_PORT', 3306)),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', ''),
                database=os.getenv('DB_NAME', 'student_management_system')
            )

            if self._connection.is_connected():
                print("✓ Database connection established successfully")
                return True
        except Error as e:
            print(f"✗ Error connecting to MySQL database: {e}")
            return False

    def disconnect(self) -> None:
        """Close database connection."""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("✓ Database connection closed")

    def execute_query(self, query: str, params: Tuple = ()) -> bool:
        """Execute a query that modifies data (INSERT, UPDATE, DELETE).

        Args:
            query: SQL query string with %s placeholders
            params: Tuple of parameters for parameterized query

        Returns:
            bool: True if query executed successfully, False otherwise
        """
        cursor = None
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            self._connection.commit()
            return True
        except Error as e:
            print(f"✗ Error executing query: {e}")
            self._connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def fetch_one(self, query: str, params: Tuple = ()) -> Optional[Tuple]:
        """Fetch a single row from database.

        Args:
            query: SQL query string with %s placeholders
            params: Tuple of parameters for parameterized query

        Returns:
            Tuple: Single row data or None if not found
        """
        cursor = None
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"✗ Error fetching data: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def fetch_all(self, query: str, params: Tuple = ()) -> List[Tuple]:
        """Fetch multiple rows from database.

        Args:
            query: SQL query string with %s placeholders
            params: Tuple of parameters for parameterized query

        Returns:
            List[Tuple]: List of rows or empty list if no results
        """
        cursor = None
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results if results else []
        except Error as e:
            print(f"✗ Error fetching data: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def is_connected(self) -> bool:
        """Check if database connection is active.

        Returns:
            bool: True if connected, False otherwise
        """
        return self._connection is not None and self._connection.is_connected()

    def get_connection(self):
        """Get the raw database connection object.

        Returns:
            Connection object or None
        """
        return self._connection
