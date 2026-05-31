-- Sample Data for Student Management System

USE student_management_system;

-- Insert Sample Students
INSERT INTO students (first_name, last_name, gender, date_of_birth, email, phone) VALUES
('John', 'Doe', 'Male', '2002-03-15', 'john.doe@university.edu', '555-0101'),
('Jane', 'Smith', 'Female', '2003-07-22', 'jane.smith@university.edu', '555-0102'),
('Michael', 'Johnson', 'Male', '2002-11-08', 'michael.johnson@university.edu', '555-0103'),
('Emily', 'Williams', 'Female', '2003-05-14', 'emily.williams@university.edu', '555-0104'),
('David', 'Brown', 'Male', '2002-09-25', 'david.brown@university.edu', '555-0105'),
('Sophia', 'Davis', 'Female', '2003-01-30', 'sophia.davis@university.edu', '555-0106'),
('Robert', 'Miller', 'Male', '2002-12-10', 'robert.miller@university.edu', '555-0107'),
('Olivia', 'Wilson', 'Female', '2003-06-18', 'olivia.wilson@university.edu', '555-0108');

-- Insert Sample Courses
INSERT INTO courses (course_name, credits) VALUES
('Introduction to Computer Science', 3),
('Data Structures and Algorithms', 4),
('Database Management Systems', 4),
('Web Development Fundamentals', 3),
('Object-Oriented Programming', 4),
('Mathematics for Computer Science', 3),
('Software Engineering', 4),
('Operating Systems', 4);

-- Insert Sample Enrollments
INSERT INTO enrollments (student_id, course_id, enrollment_date) VALUES
(1, 1, '2024-01-15'),
(1, 2, '2024-01-15'),
(1, 3, '2024-01-16'),
(2, 1, '2024-01-15'),
(2, 4, '2024-01-16'),
(2, 5, '2024-01-17'),
(3, 2, '2024-01-16'),
(3, 3, '2024-01-16'),
(3, 6, '2024-01-17'),
(4, 1, '2024-01-18'),
(4, 4, '2024-01-18'),
(4, 7, '2024-01-19'),
(5, 2, '2024-01-19'),
(5, 5, '2024-01-19'),
(5, 8, '2024-01-20'),
(6, 3, '2024-01-20'),
(6, 4, '2024-01-20'),
(6, 7, '2024-01-21'),
(7, 1, '2024-01-21'),
(7, 6, '2024-01-21'),
(8, 5, '2024-01-22'),
(8, 8, '2024-01-22');
