# Student Management System

A comprehensive student management system built with Python and MySQL that provides an intuitive interface for managing students, courses, and enrollments.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Software Requirements](#software-requirements)
- [Installation Instructions](#installation-instructions)
- [Database Setup](#database-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage Examples](#usage-examples)
- [Features Overview](#features-overview)

## Features

### Student Management
- Add new students with validation
- Update student information
- Delete student records
- Search students by ID, email, or name
- View all students in the system

### Course Management
- Add new courses with credit values
- Update course information
- Delete courses
- Search courses by ID or name
- View all available courses

### Enrollment Management
- Enroll students in courses
- Remove enrollments
- View all courses for a specific student
- View all students enrolled in a specific course
- View complete enrollment records

### Reports
- Summary statistics (total students, courses, enrollments)
- Student enrollment report with course details
- Course enrollment report with student details
- Student total credits report
- Enrollment statistics and analysis

## Project Structure

```
StudentManagementSystem/
│
├── database/
│   ├── schema.sql          # Database schema and table definitions
│   └── sample_data.sql     # Sample data for testing
│
├── src/
│   ├── db_connection.py    # Database connection management
│   ├── student.py          # Student operations and validation
│   ├── course.py           # Course operations and validation
│   ├── enrollment.py       # Enrollment operations
│   ├── reports.py          # Reporting functionality
│   └── main.py             # Main application entry point
│
├── requirements.txt        # Python package dependencies
├── .env.example            # Example environment configuration
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## Software Requirements

- **Python 3.11 or higher**
- **MySQL 5.7 or higher** (or MySQL 8.0+)
- **pip** (Python package manager)
- **Terminal/Command Prompt** access

## Installation Instructions

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd StudentManagementSystem

# Or manually download and extract the project folder
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `mysql-connector-python` - MySQL database connector for Python
- `python-dotenv` - Environment variable management

### Step 3: Configure Environment Variables

1. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

2. Edit `.env` file with your MySQL credentials:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=student_management_system
```

## Database Setup

### Step 1: Start MySQL Server

**On Windows:**
```bash
# Start MySQL service
net start MySQL80
```

**On macOS:**
```bash
# Using Homebrew
brew services start mysql
```

**On Linux:**
```bash
# Using systemctl
sudo systemctl start mysql
```

### Step 2: Create Database and Tables

1. Connect to MySQL:

```bash
mysql -u root -p
```

2. Enter your MySQL password when prompted.

3. Run the schema file:

```sql
SOURCE database/schema.sql;
```

4. (Optional) Load sample data:

```sql
SOURCE database/sample_data.sql;
```

5. Exit MySQL:

```sql
EXIT;
```

### Step 3: Verify Database Creation

```bash
mysql -u root -p -e "USE student_management_system; SHOW TABLES;"
```

You should see three tables:
- `students`
- `courses`
- `enrollments`

## Configuration

### Environment Variables

Edit the `.env` file to configure your database connection:

```env
# Database Host
DB_HOST=localhost

# Database Port (default MySQL port)
DB_PORT=3306

# MySQL Username
DB_USER=root

# MySQL Password
DB_PASSWORD=your_password

# Database Name
DB_NAME=student_management_system
```

### Database Configuration

If you need to use a different MySQL server or credentials:

1. Update the `.env` file with correct credentials
2. Ensure the MySQL server is running and accessible
3. Verify the database exists by running:

```bash
mysql -u root -p -e "SHOW DATABASES LIKE 'student_management_system';"
```

## Running the Application

### Start the Application

```bash
python src/main.py
```

You should see the main menu:

```
============================================================
STUDENT MANAGEMENT SYSTEM
============================================================

1. Student Management
2. Course Management
3. Enrollment Management
4. Reports
5. Exit

------------------------------------------------------------
```

### Navigation

- Use the number keys to navigate between menus
- Follow the on-screen prompts to enter information
- Enter 0 or select "Back" to return to previous menus
- Select "Exit" to close the application

## Usage Examples

### Example 1: Add a Student

```
1. Press 1 (Student Management)
2. Press 1 (Add Student)
3. Enter: John
4. Enter: Doe
5. Enter: Male
6. Enter: 2002-03-15
7. Enter: john.doe@university.edu
8. Enter: 555-0101
```

### Example 2: Add a Course

```
1. Press 2 (Course Management)
2. Press 1 (Add Course)
3. Enter: Introduction to Computer Science
4. Enter: 3
```

### Example 3: Enroll Student in Course

```
1. Press 3 (Enrollment Management)
2. Press 1 (Enroll Student in Course)
3. Enter Student ID: 1
4. Enter Course ID: 1
```

### Example 4: View Reports

```
1. Press 4 (Reports)
2. Select desired report option
```

## Features Overview

### Input Validation

The system validates all inputs:
- **Email**: Must be a valid email format
- **Phone**: Minimum 7 characters, numeric format
- **Date**: Must be YYYY-MM-DD format
- **Credits**: Must be positive integers
- **Duplicate Prevention**: Prevents duplicate emails and course names

### Security Features

- **Parameterized Queries**: Prevents SQL injection attacks
- **Database Constraints**: Enforces data integrity
- **Foreign Key Relationships**: Maintains referential integrity
- **Unique Constraints**: Prevents duplicate entries

### Data Management

- **Cascading Deletes**: Deleting a student removes all related enrollments
- **Atomic Transactions**: Ensures data consistency
- **Error Handling**: Comprehensive error messages
- **Logging**: Records all operations

### Performance Features

- **Indexed Columns**: Fast searches on frequently queried fields
- **Optimized Queries**: Efficient JOIN operations
- **Connection Management**: Proper database connection handling

## Troubleshooting

### Issue: "Can't connect to MySQL server"

**Solution:**
1. Ensure MySQL is running
2. Check `.env` file has correct credentials
3. Verify MySQL is accessible on localhost:3306
4. Check if firewall is blocking the connection

### Issue: "Database does not exist"

**Solution:**
1. Run schema.sql file: `SOURCE database/schema.sql;`
2. Verify database creation: `SHOW DATABASES;`
3. Check DB_NAME in .env file

### Issue: "Module not found" errors

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Issue: "Permission denied" on database operations

**Solution:**
1. Verify MySQL user has correct permissions
2. Check user credentials in .env file
3. Run the following in MySQL:

```sql
GRANT ALL PRIVILEGES ON student_management_system.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

## Database Schema

### Students Table
- `student_id` - Primary key, auto-increment
- `first_name` - Student's first name
- `last_name` - Student's last name
- `gender` - Gender information
- `date_of_birth` - Date of birth
- `email` - Email address (unique)
- `phone` - Phone number
- `created_at` - Record creation timestamp
- `updated_at` - Record update timestamp

### Courses Table
- `course_id` - Primary key, auto-increment
- `course_name` - Name of the course
- `credits` - Number of credits
- `created_at` - Record creation timestamp
- `updated_at` - Record update timestamp

### Enrollments Table
- `enrollment_id` - Primary key, auto-increment
- `student_id` - Foreign key to students table
- `course_id` - Foreign key to courses table
- `enrollment_date` - Date of enrollment
- `created_at` - Record creation timestamp

## Best Practices

1. **Regular Backups**: Backup your database regularly
2. **Data Validation**: The system validates all inputs
3. **Access Control**: Use strong MySQL passwords
4. **Environment Security**: Don't commit `.env` file to version control
5. **Database Maintenance**: Run regular maintenance on your MySQL server

## Technical Details

- **Language**: Python 3.11+
- **Database**: MySQL 5.7+
- **Architecture**: Object-oriented programming (OOP)
- **Pattern**: Module-based architecture
- **Query Type**: Parameterized queries for security
- **Error Handling**: Try-except blocks with meaningful messages
- **Connection Pool**: Managed database connections

## Support and Contribution

For issues, suggestions, or contributions, please refer to the project repository.

## License

This project is provided as-is for educational and commercial use.

## Version History

### Version 1.0.0 (Initial Release)
- Complete student management system
- Full CRUD operations for students, courses, and enrollments
- Comprehensive reporting system
- Input validation and error handling
- Database schema and sample data

---

**Last Updated**: 2024
**Created for**: Educational and Commercial Use
