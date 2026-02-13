-- CRM Database Schema for SQLite
-- This script creates the necessary tables for the CRM application
-- Compatible with SQLite for local testing

-- Tasks table for follow-up activities
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NULL,
    title TEXT NOT NULL,
    description TEXT NULL,
    due_date DATETIME NULL,
    assigned_to TEXT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    priority TEXT NOT NULL DEFAULT 'medium',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);

-- KPIs table for tracking key performance indicators
CREATE TABLE IF NOT EXISTS kpis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NULL,
    calculation_method TEXT NULL,
    target_value REAL NOT NULL DEFAULT 0,
    current_value REAL NOT NULL DEFAULT 0,
    period TEXT NOT NULL DEFAULT 'monthly',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_kpis_period ON kpis(period);

-- Targets table for tracking goals
CREATE TABLE IF NOT EXISTS targets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NULL,
    target_type TEXT NOT NULL,
    target_value REAL NOT NULL,
    current_value REAL NOT NULL DEFAULT 0,
    start_date DATETIME NULL,
    end_date DATETIME NULL,
    status TEXT NOT NULL DEFAULT 'active',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_targets_status ON targets(status);
CREATE INDEX IF NOT EXISTS idx_targets_end_date ON targets(end_date);

-- Notes table for customer notes
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    note_text TEXT NOT NULL,
    created_by TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_notes_customer_id ON notes(customer_id);

-- Sample ERP Tables for Testing (optional)
-- Customers table (simulating ERP data)
CREATE TABLE IF NOT EXISTS Customers (
    CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerName TEXT NOT NULL,
    Email TEXT,
    Phone TEXT,
    Address TEXT,
    City TEXT,
    Country TEXT,
    CreatedDate DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Sales table (simulating ERP data)
CREATE TABLE IF NOT EXISTS Sales (
    SaleID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerID INTEGER,
    SaleDate DATETIME NOT NULL,
    TotalAmount REAL NOT NULL,
    ProductName TEXT,
    Quantity INTEGER,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
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
    (1, 'Follow up on proposal', 'Contact customer about submitted proposal', datetime('now', '+2 days'), 'John Smith', 'pending', 'high'),
    (2, 'Schedule product demo', 'Set up demo meeting for next week', datetime('now', '+5 days'), 'Jane Doe', 'pending', 'medium'),
    (3, 'Send contract for signature', 'Email final contract documents', datetime('now', '+1 day'), 'John Smith', 'pending', 'urgent'),
    (1, 'Quarterly business review', 'Schedule QBR meeting with key stakeholder', datetime('now', '+30 days'), 'Jane Doe', 'pending', 'medium');

-- Sample Notes
INSERT INTO notes (customer_id, note_text, created_by)
VALUES 
    (1, 'Customer expressed interest in enterprise plan. Follow up next week.', 'John Smith'),
    (2, 'Demo went well. Waiting for decision from management team.', 'Jane Doe'),
    (3, 'Contract negotiations in progress. Expecting signature by end of week.', 'John Smith');

-- Sample ERP Customers
INSERT INTO Customers (CustomerName, Email, Phone, Address, City, Country)
VALUES 
    ('Acme Corporation', 'contact@acme.com', '555-0100', '123 Main St', 'New York', 'USA'),
    ('TechStart Inc', 'info@techstart.com', '555-0200', '456 Tech Ave', 'San Francisco', 'USA'),
    ('Global Solutions Ltd', 'hello@globalsolutions.com', '555-0300', '789 Business Blvd', 'London', 'UK'),
    ('Innovation Labs', 'contact@innovationlabs.com', '555-0400', '321 Innovation Dr', 'Austin', 'USA'),
    ('Digital Dynamics', 'sales@digitaldynamics.com', '555-0500', '654 Digital Way', 'Seattle', 'USA');

-- Sample ERP Sales
INSERT INTO Sales (CustomerID, SaleDate, TotalAmount, ProductName, Quantity)
VALUES 
    (1, datetime('now', '-10 days'), 5000.00, 'Product A', 10),
    (2, datetime('now', '-8 days'), 3500.00, 'Product B', 7),
    (1, datetime('now', '-5 days'), 7500.00, 'Product C', 15),
    (3, datetime('now', '-3 days'), 2000.00, 'Product A', 4),
    (4, datetime('now', '-2 days'), 6000.00, 'Product B', 12),
    (2, datetime('now', '-1 day'), 4200.00, 'Product C', 8),
    (5, datetime('now'), 8500.00, 'Product A', 17);
