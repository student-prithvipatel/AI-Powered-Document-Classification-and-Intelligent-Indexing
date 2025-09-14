-- Create database
CREATE DATABASE doc_ai;
USE doc_ai;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL
);

-- Documents table
CREATE TABLE documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    author VARCHAR(100),
    doc_date VARCHAR(20),
    category VARCHAR(50),
    summary TEXT,
    role VARCHAR(20),
    filepath VARCHAR(255)
);

-- Insert demo users
INSERT INTO users (username, password, role) VALUES
('admin', 'admin123', 'Admin'),
('hruser', 'hr123', 'HR'),
('financeuser', 'fin123', 'Finance'),
('legaluser', 'legal123', 'Legal');
