-- Create database if not exists
CREATE DATABASE IF NOT EXISTS fastapidb;

-- Use the database
USE fastapidb;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO users (name, email) VALUES 
    ('John Doe', 'john@example.com'),
    ('Jane Smith', 'jane@example.com'),
    ('Bob Johnson', 'bob@example.com')
ON DUPLICATE KEY UPDATE name=name;

-- Create a test table
CREATE TABLE IF NOT EXISTS app_info (
    id INT AUTO_INCREMENT PRIMARY KEY,
    app_name VARCHAR(255) NOT NULL,
    version VARCHAR(50) NOT NULL,
    deployment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert app info
INSERT INTO app_info (app_name, version) VALUES 
    ('FastAPI MySQL DevOps', '1.0.0')
ON DUPLICATE KEY UPDATE version=version;