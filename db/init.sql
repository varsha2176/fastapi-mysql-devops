CREATE DATABASE IF NOT EXISTS testdb;
USE testdb;

-- Users table with more fields for admin panel
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role ENUM('admin', 'user', 'moderator') DEFAULT 'user',
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO users (name, email, role, status) VALUES
('Admin User', 'admin@example.com', 'admin', 'active'),
('John Doe', 'john@example.com', 'user', 'active'),
('Jane Smith', 'jane@example.com', 'moderator', 'active'),
('Bob Wilson', 'bob@example.com', 'user', 'inactive');