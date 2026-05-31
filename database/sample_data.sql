-- Sample Data for Student Management System
-- Insert sample students, courses, and enrollments

USE student_management_system;

-- Insert Sample Students
INSERT INTO students (first_name, last_name, gender, date_of_birth, email, phone) VALUES
('John', 'Doe', 'Male', '2005-03-15', 'john.doe@example.com', '555-0101'),
('Jane', 'Smith', 'Female', '2004-07-22', 'jane.smith@example.com', '555-0102'),
('Michael', 'Johnson', 'Male', '2005-11-10', 'michael.johnson@example.com', '555-0103'),
('Emily', 'Williams', 'Female', '2004-05-30', 'emily.williams@example.com', '555-0104'),
('David', 'Brown', 'Male', '2005-01-18', 'david.brown@example.com', '555-0105'),
('Sarah', 'Davis', 'Female', '2004-09-25', 'sarah.davis@example.com', '555-0106'),
('Robert', 'Miller', 'Male', '2005-06-12', 'robert.miller@example.com', '555-0107'),
('Jessica', 'Wilson', 'Female', '2004-12-08', 'jessica.wilson@example.com', '555-0108'),
('James', 'Moore', 'Male', '2005-02-14', 'james.moore@example.com', '555-0109'),
('Lisa', 'Taylor', 'Female', '2004-08-20', 'lisa.taylor@example.com', '555-0110');

-- Insert Sample Courses
INSERT INTO courses (course_name, credits, description) VALUES
('Introduction to Python', 3, 'Learn the basics of Python programming'),
('Database Design', 4, 'Master SQL and relational database concepts'),
('Web Development', 3, 'Build responsive web applications'),
('Data Structures', 4, 'Understand fundamental data structures and algorithms'),
('Operating Systems', 3, 'Learn OS concepts and implementation'),
('Machine Learning', 4, 'Introduction to ML algorithms and applications'),
('Software Engineering', 3, 'Software development practices and methodologies'),
('Cloud Computing', 3, 'AWS and cloud infrastructure basics');

-- Insert Sample Enrollments
INSERT INTO enrollments (student_id, course_id, enrollment_date, grade) VALUES
(1, 1, '2025-01-15', 'A'),
(1, 2, '2025-01-15', 'B+'),
(1, 4, '2025-01-20', 'A-'),
(2, 1, '2025-01-15', 'A-'),
(2, 3, '2025-01-18', 'A'),
(2, 6, '2025-01-20', 'B'),
(3, 2, '2025-01-16', 'B'),
(3, 5, '2025-01-16', 'B+'),
(3, 8, '2025-01-22', 'A'),
(4, 1, '2025-01-17', 'A'),
(4, 3, '2025-01-17', 'A-'),
(4, 7, '2025-01-21', 'B+'),
(5, 4, '2025-01-19', 'B'),
(5, 6, '2025-01-19', 'A-'),
(6, 2, '2025-01-20', 'A'),
(6, 5, '2025-01-20', 'B'),
(7, 1, '2025-01-21', 'B+'),
(7, 8, '2025-01-21', 'A'),
(8, 3, '2025-01-22', 'A-'),
(8, 6, '2025-01-22', 'B+'),
(9, 2, '2025-01-23', 'A'),
(9, 7, '2025-01-23', 'A'),
(10, 4, '2025-01-24', 'B'),
(10, 8, '2025-01-24', 'A-');