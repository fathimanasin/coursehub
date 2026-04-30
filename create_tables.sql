-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS course_db;

-- Use the course_db database
USE course_db;

-- Create the Departments table if it doesn't exist
CREATE TABLE IF NOT EXISTS Departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Create the Students table if it doesn't exist
CREATE TABLE IF NOT EXISTS Students (
    student_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

-- Create the Instructors table if it doesn't exist
CREATE TABLE IF NOT EXISTS Instructors (
    instructor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);

-- Create the Courses table and include instructor_id column if it doesn't exist
CREATE TABLE IF NOT EXISTS Courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    credits INT NOT NULL,
    department_id INT,
    instructor_id INT,  -- Added instructor_id for reference to the Instructors table
    FOREIGN KEY (department_id) REFERENCES Departments(department_id),
    FOREIGN KEY (instructor_id) REFERENCES Instructors(instructor_id)  -- Foreign key reference to Instructors table
);

-- Create the Enrollments table if it doesn't exist
CREATE TABLE IF NOT EXISTS Enrollments (
    student_id INT,
    course_id INT,
    semester VARCHAR(20) NOT NULL,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);

-- Sample Data Insertion

-- Insert departments if they don't already exist
INSERT IGNORE INTO Departments (name) 
VALUES 
    ('Computer Science'),
    ('Mathematics');

-- Insert students if they don't already exist
INSERT IGNORE INTO Students (student_id, name, email) 
VALUES 
    (1, 'Alice', 'alice@example.com'),
    (2, 'Bob', 'bob@example.com');

-- Insert instructors if they don't already exist
INSERT IGNORE INTO Instructors (name, email, department_id) 
VALUES 
    ('Dr. Smith', 'smith@university.edu', 1),
    ('Prof. Johnson', 'johnson@university.edu', 2);

-- Insert courses if they don't already exist
INSERT IGNORE INTO Courses (title, credits, department_id, instructor_id) 
VALUES 
    ('Database Systems', 4, 1, 1),  -- Course 1 with instructor Dr. Smith
    ('Algorithms', 3, 1, 1),       -- Course 2 with instructor Dr. Smith
    ('Calculus', 3, 2, 2);         -- Course 3 with instructor Prof. Johnson
