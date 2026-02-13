# Quick Start Guide

This guide will help you get the CRM application up and running quickly.

## Option 1: Manual Setup (Recommended for Development)

### Step 1: Prerequisites

Ensure you have:
- Python 3.8+ installed
- Node.js 16+ installed
- Microsoft SQL Server with both ERP and CRM databases
- ODBC Driver 17 for SQL Server installed

### Step 2: Run Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Configure Environment

Edit `backend/.env` with your database credentials:

```bash
nano backend/.env
```

### Step 4: Create CRM Database Tables

Connect to your SQL Server and run the schema:

```bash
sqlcmd -S your-crm-server -d crm_database -U crm_user -P password -i backend/schema.sql
```

Or use SQL Server Management Studio (SSMS) to execute `backend/schema.sql`.

### Step 5: Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Option 2: Docker Setup (Recommended for Production)

### Step 1: Configure Environment

Create a `.env` file in the root directory based on `backend/.env.example`.

### Step 2: Build and Start

```bash
docker-compose up -d
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

### Step 3: View Logs

```bash
docker-compose logs -f
```

### Step 4: Stop Application

```bash
docker-compose down
```

## Initial Login / Setup

1. Open http://localhost:3000 in your browser
2. Navigate to different sections:
   - **Dashboard**: Overview of metrics
   - **Customers**: View ERP customer data
   - **Tasks**: Create and manage tasks
   - **KPIs**: Define and track KPIs
   - **Targets**: Set and monitor targets
   - **Analytics**: View sales charts and reports

## Sample Data

The `schema.sql` includes sample data for:
- 4 KPIs (Monthly Sales Revenue, Customer Acquisition, etc.)
- 3 Targets (Q1 Revenue, Annual Growth, etc.)
- 4 Tasks (Follow-ups, demos, etc.)
- 3 Customer notes

You can modify or delete this sample data as needed.

## Troubleshooting

### Backend won't start

**Issue:** Database connection error

**Solution:**
1. Verify database server is accessible
2. Check credentials in `.env` file
3. Ensure ODBC Driver 17 for SQL Server is installed
4. Check firewall settings

**Issue:** Module not found

**Solution:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend won't start

**Issue:** npm install fails

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Issue:** Cannot connect to API

**Solution:**
1. Verify backend is running on port 5000
2. Check browser console for CORS errors
3. Verify `CORS_ORIGINS` in backend `.env` includes your frontend URL

### No ERP data showing

The application is designed to connect to an existing ERP database. If you don't have one:

1. You can still use all CRM features (Tasks, KPIs, Targets)
2. The Customers and Sales pages will show empty data
3. To test with sample data, you can create sample ERP tables:

```sql
-- Create sample ERP tables in a test database
CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    CustomerName NVARCHAR(255),
    Email NVARCHAR(255),
    Phone NVARCHAR(50),
    Address NVARCHAR(255),
    City NVARCHAR(100),
    Country NVARCHAR(100)
);

CREATE TABLE Sales (
    SaleID INT PRIMARY KEY,
    CustomerID INT,
    SaleDate DATETIME,
    TotalAmount DECIMAL(18,2),
    ProductName NVARCHAR(255),
    Quantity INT
);

-- Insert sample data
INSERT INTO Customers VALUES 
(1, 'Acme Corp', 'contact@acme.com', '555-0100', '123 Main St', 'New York', 'USA'),
(2, 'TechStart Inc', 'info@techstart.com', '555-0200', '456 Tech Ave', 'San Francisco', 'USA');

INSERT INTO Sales VALUES
(1, 1, '2024-01-15', 5000.00, 'Product A', 10),
(2, 2, '2024-01-20', 3500.00, 'Product B', 7);
```

## Next Steps

1. **Customize ERP Queries**: Update queries in `backend/app/services/erp_service.py` to match your ERP schema
2. **Add Authentication**: Implement user authentication for API endpoints
3. **Deploy to Production**: Use gunicorn for backend and nginx for frontend
4. **Set Up Monitoring**: Add logging and monitoring for production use
5. **Create Backups**: Set up regular database backups

## Getting Help

- Check the main README.md for detailed documentation
- Review API documentation in README.md
- Check logs for error messages
- Ensure all prerequisites are installed correctly
