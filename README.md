# Student Management System

A comprehensive Python-based Student Management System with MySQL database integration. This application provides complete functionality for managing students, courses, and enrollment records with an intuitive command-line interface.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Software Requirements](#software-requirements)
- [Installation](#installation)
- [Database Setup](#database-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Usage Examples](#usage-examples)
- [Project Architecture](#project-architecture)

## ✨ Features

### Student Management
- ✅ Add new students with validation
- ✅ View all students
- ✅ Search students by ID or name
- ✅ Update student information
- ✅ Delete students (with cascade delete for enrollments)

### Course Management
- ✅ Add new courses
- ✅ View all courses
- ✅ Search courses by name
- ✅ Update course information
- ✅ Delete courses

### Enrollment Management
- ✅ Enroll students in courses
- ✅ View courses for a specific student
- ✅ View students in a specific course
- ✅ View all enrollments
- ✅ Remove enrollments
- ✅ Update student grades

### Reporting
- ✅ System statistics (total students, courses, enrollments)
- ✅ Student enrollment reports
- ✅ Course enrollment reports
- ✅ Top enrolled courses
- ✅ Grade distribution analysis

## 📁 Project Structure

```
StudentManagementSystem/
├── database/
│   ├── schema.sql              # Database schema with tables and views
│   └── sample_data.sql         # Sample data for testing
├── src/
│   ├── db_connection.py        # Database connection management (Singleton pattern)
│   ├── student.py              # Student management class
│   ├── course.py               # Course management class
│   ├── enrollment.py           # Enrollment management class
│   ├── reports.py              # Reporting and analytics
│   └── main.py                 # Main application with CLI menu
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 💻 Software Requirements

- Python 3.11 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

## 🚀 Installation

### Step 1: Clone or Download the Project

```bash
cd StudentManagementSystem
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `mysql-connector-python` - MySQL database connector
- `python-dotenv` - Environment variable management

## 🗄️ Database Setup

### Step 1: Create the Database and Tables

1. Open MySQL Command Line Client or MySQL Workbench:

```bash
mysql -u root -p
```

2. Execute the schema file:

```sql
source database/schema.sql;
```

This will create:
- `student_management_system` database
- `students` table
- `courses` table
- `enrollments` table
- `student_enrollment_report` view

### Step 2: Insert Sample Data (Optional)

To populate the database with sample data for testing:

```sql
source database/sample_data.sql;
```

This inserts:
- 10 sample students
- 8 sample courses
- 24 sample enrollments with grades

## ⚙️ Configuration

### Step 1: Create Environment Variables File

1. Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

2. Edit `.env` with your database credentials:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=student_management_system
```

**Replace:**
- `your_mysql_password` - Your MySQL root password
- Other values if your database configuration differs

## ▶️ Running the Application

### Start the Application

```bash
python src/main.py
```

### Expected Output

```
✓ Database connection established successfully
✓ Welcome to the Student Management System!

============================================================
     STUDENT MANAGEMENT SYSTEM
============================================================

1. Student Management
2. Course Management
3. Enrollment Management
4. Generate Reports
5. Exit
------------------------------------------------------------
Select an option:
```

## 📖 Usage Examples

### Adding a Student

1. From main menu, select `1` (Student Management)
2. Select `1` (Add Student)
3. Enter student details:
   ```
   First Name: John
   Last Name: Doe
   Email: john.doe@example.com
   Gender: Male
   Date of Birth: 2005-03-15
   Phone: 555-0101
   ```
4. Confirmation: `✓ Student added successfully with ID: 11`

### Enrolling a Student

1. From main menu, select `3` (Enrollment Management)
2. Select `1` (Enroll Student)
3. Enter enrollment details:
   ```
   Enter Student ID: 1
   Enter Course ID: 2
   Enrollment Date (YYYY-MM-DD) [optional]: 2025-02-01
   ```
4. Confirmation: `✓ Student 1 enrolled in Course 2 successfully`

### Generating Reports

1. From main menu, select `4` (Generate Reports)
2. Choose report type:
   - System Statistics
   - Student Enrollment Report
   - Course Enrollment Report
   - Top Enrolled Courses
   - Grade Distribution

### Updating Student Grade

1. From main menu, select `3` (Enrollment Management)
2. Select `6` (Update Grade)
3. Enter:
   ```
   Enter Student ID: 1
   Enter Course ID: 2
   Enter Grade (A, A-, B+, B, B-, C+, C, C-, D, F): A
   ```
4. Confirmation: `✓ Grade updated successfully for Student 1 in Course 2`

## 🏗️ Project Architecture

### Design Patterns Used

1. **Singleton Pattern** - Database connection management ensures only one connection instance
2. **OOP Principles** - Classes for Student, Course, Enrollment, and Reports
3. **Separation of Concerns** - Each module handles specific functionality
4. **MVC Pattern** - Main.py acts as controller, database modules as model

### Key Features

- **Parameterized Queries** - Prevents SQL injection attacks
- **Exception Handling** - Comprehensive error handling throughout
- **Input Validation** - Email format, date format, and credit validation
- **Cascading Deletes** - Foreign key constraints ensure data integrity
- **Efficient Indexing** - Database indexes for faster queries
- **Code Documentation** - Docstrings for all methods and classes

### Database Schema Highlights

```sql
-- Students Table
student_id (PK, AUTO_INCREMENT)
first_name (VARCHAR, NOT NULL)
last_name (VARCHAR, NOT NULL)
email (VARCHAR, UNIQUE, NOT NULL)
... additional fields ...

-- Courses Table
course_id (PK, AUTO_INCREMENT)
course_name (VARCHAR, NOT NULL)
credits (INT, 1-10)

-- Enrollments Table
enrollment_id (PK, AUTO_INCREMENT)
student_id (FK → students)
course_id (FK → courses)
enrollment_date (DATE)
grade (VARCHAR, optional)
```

## 🔒 Security Features

- **Parameterized Queries** - All SQL queries use parameterized statements
- **Environment Variables** - Database credentials stored in `.env` (not in code)
- **Input Validation** - Email and date format validation
- **Foreign Key Constraints** - Referential integrity
- **Unique Constraints** - Email uniqueness, enrollment uniqueness

## 🐛 Troubleshooting

### Connection Error

**Error:** `Error connecting to MySQL database: Access denied for user 'root'@'localhost'`

**Solution:**
1. Check MySQL is running
2. Verify credentials in `.env` file
3. Ensure MySQL user has required permissions

### Database Not Found

**Error:** `Unknown database 'student_management_system'`

**Solution:**
1. Run `source database/schema.sql;` from MySQL client
2. Verify database is created: `SHOW DATABASES;`

### Module Not Found

**Error:** `ModuleNotFoundError: No module named 'mysql'`

**Solution:**
```bash
pip install -r requirements.txt
```

## 📝 Notes

- All dates should be in `YYYY-MM-DD` format
- Credits must be between 1 and 10
- Valid grades: A, A-, B+, B, B-, C+, C, C-, D, F
- Email addresses must be unique in the system
- Deleting a student automatically removes all their enrollments

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review code comments and docstrings
3. Verify database schema is correctly created
4. Ensure environment variables are properly configured

## 📄 License

This project is open source and available for educational purposes.

---

**Version:** 1.0.0  
**Last Updated:** 2025-05-31  
**Author:** Student Management System Team
