-- CRM Database Schema
-- This script creates the necessary tables for the CRM application
-- Run this on your CRM SQL Server database

-- Tasks table for follow-up activities
CREATE TABLE tasks (
    id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT NULL,
    title NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX) NULL,
    due_date DATETIME NULL,
    assigned_to NVARCHAR(100) NULL,
    status NVARCHAR(50) NOT NULL DEFAULT 'pending',
    priority NVARCHAR(50) NOT NULL DEFAULT 'medium',
    created_at DATETIME NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME NOT NULL DEFAULT GETDATE(),
    INDEX idx_status (status),
    INDEX idx_assigned_to (assigned_to),
    INDEX idx_due_date (due_date)
);

-- KPIs table for tracking key performance indicators
CREATE TABLE kpis (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX) NULL,
    calculation_method NVARCHAR(MAX) NULL,
    target_value DECIMAL(18, 2) NOT NULL DEFAULT 0,
    current_value DECIMAL(18, 2) NOT NULL DEFAULT 0,
    period NVARCHAR(50) NOT NULL DEFAULT 'monthly',
    created_at DATETIME NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME NOT NULL DEFAULT GETDATE(),
    INDEX idx_period (period)
);

-- Targets table for tracking goals
CREATE TABLE targets (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX) NULL,
    target_type NVARCHAR(100) NOT NULL,
    target_value DECIMAL(18, 2) NOT NULL,
    current_value DECIMAL(18, 2) NOT NULL DEFAULT 0,
    start_date DATETIME NULL,
    end_date DATETIME NULL,
    status NVARCHAR(50) NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME NOT NULL DEFAULT GETDATE(),
    INDEX idx_status (status),
    INDEX idx_end_date (end_date)
);

-- Notes table for customer notes
CREATE TABLE notes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    customer_id INT NOT NULL,
    note_text NVARCHAR(MAX) NOT NULL,
    created_by NVARCHAR(100) NOT NULL,
    created_at DATETIME NOT NULL DEFAULT GETDATE(),
    INDEX idx_customer_id (customer_id)
);

-- Insert sample data for demonstration

-- Sample KPIs
INSERT INTO kpis (name, description, calculation_method, target_value, current_value, period)
VALUES 
    ('Monthly Sales Revenue', 'Total sales revenue for the current month', 'SUM(sales.amount)', 100000, 75000, 'monthly'),
    ('Customer Acquisition', 'Number of new customers acquired this month', 'COUNT(new_customers)', 50, 35, 'monthly'),
    ('Task Completion Rate', 'Percentage of tasks completed on time', '(completed_tasks / total_tasks) * 100', 90, 85, 'monthly'),
    ('Average Deal Size', 'Average value of closed deals', 'AVG(deal_value)', 5000, 4500, 'monthly');

-- Sample Targets
INSERT INTO targets (name, description, target_type, target_value, current_value, start_date, end_date, status)
VALUES 
    ('Q1 2024 Revenue Target', 'Revenue goal for first quarter', 'revenue', 300000, 180000, '2024-01-01', '2024-03-31', 'active'),
    ('Annual Customer Growth', 'New customer acquisition goal for 2024', 'customers', 500, 280, '2024-01-01', '2024-12-31', 'active'),
    ('Monthly Task Completion', 'Complete 100 tasks this month', 'tasks', 100, 65, '2024-01-01', '2024-01-31', 'active');

-- Sample Tasks
INSERT INTO tasks (customer_id, title, description, due_date, assigned_to, status, priority)
VALUES 
    (1, 'Follow up on proposal', 'Contact customer about submitted proposal', DATEADD(day, 2, GETDATE()), 'John Smith', 'pending', 'high'),
    (2, 'Schedule product demo', 'Set up demo meeting for next week', DATEADD(day, 5, GETDATE()), 'Jane Doe', 'pending', 'medium'),
    (3, 'Send contract for signature', 'Email final contract documents', DATEADD(day, 1, GETDATE()), 'John Smith', 'pending', 'urgent'),
    (1, 'Quarterly business review', 'Schedule QBR meeting with key stakeholder', DATEADD(day, 30, GETDATE()), 'Jane Doe', 'pending', 'medium');

-- Sample Notes
INSERT INTO notes (customer_id, note_text, created_by)
VALUES 
    (1, 'Customer expressed interest in enterprise plan. Follow up next week.', 'John Smith'),
    (2, 'Demo went well. Waiting for decision from management team.', 'Jane Doe'),
    (3, 'Contract negotiations in progress. Expecting signature by end of week.', 'John Smith');

PRINT 'CRM database schema created successfully!';
