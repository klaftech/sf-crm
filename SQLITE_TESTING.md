# SQLite Testing Guide

This guide explains how to use SQLite for local testing instead of SQL Server, making development and testing much easier without requiring a SQL Server instance.

## Quick Start

### 1. Initialize SQLite Databases

```bash
cd backend
python init_sqlite.py
```

This creates two SQLite database files with sample data:
- `crm_test.db` - CRM data (tasks, KPIs, targets, notes)
- `erp_test.db` - ERP data (customers, sales)

### 2. Configure Environment

Create or update your `backend/.env` file:

```bash
# Set database type to sqlite
DB_TYPE=sqlite

# SQLite database paths (these are the defaults)
SQLITE_CRM_DB_PATH=crm_test.db
SQLITE_ERP_DB_PATH=erp_test.db

# Flask configuration
FLASK_APP=app
FLASK_ENV=development
FLASK_SECRET_KEY=dev-secret-key-for-testing

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 3. Run the Application

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python app.py
```

The application will now use SQLite instead of SQL Server!

## Switching Between SQLite and SQL Server

The application supports both database types and can be switched easily via the `DB_TYPE` environment variable.

### For Testing (SQLite)

In your `.env` file:
```bash
DB_TYPE=sqlite
SQLITE_CRM_DB_PATH=crm_test.db
SQLITE_ERP_DB_PATH=erp_test.db
```

### For Production (SQL Server)

In your `.env` file:
```bash
DB_TYPE=sqlserver

# SQL Server Configuration
CRM_DB_SERVER=your-crm-server.database.windows.net
CRM_DB_NAME=crm_database
CRM_DB_USERNAME=crm_user
CRM_DB_PASSWORD=your-password
CRM_DB_DRIVER=ODBC Driver 17 for SQL Server

ERP_DB_SERVER=your-erp-server.database.windows.net
ERP_DB_NAME=erp_database
ERP_DB_USERNAME=readonly_user
ERP_DB_PASSWORD=your-password
ERP_DB_DRIVER=ODBC Driver 17 for SQL Server
```

## Benefits of SQLite for Testing

✅ **No SQL Server Required** - Test without installing SQL Server  
✅ **Fast Setup** - Initialize databases in seconds  
✅ **Easy Reset** - Just re-run `init_sqlite.py` to reset data  
✅ **Portable** - Database is a single file  
✅ **CI/CD Friendly** - Perfect for automated testing  
✅ **No Network** - Everything runs locally  

## Sample Data Included

The SQLite initialization includes sample data for testing:

### CRM Database (`crm_test.db`)
- **4 KPIs**: Monthly Sales Revenue, Customer Acquisition, Task Completion Rate, Average Deal Size
- **3 Targets**: Q1 Revenue, Annual Customer Growth, Monthly Tasks
- **4 Tasks**: Various follow-up tasks with different priorities
- **3 Notes**: Sample customer notes

### ERP Database (`erp_test.db`)
- **5 Customers**: Sample companies with contact information
- **7 Sales**: Recent sales transactions

## Database Schema Differences

The SQLite schema (`schema_sqlite.sql`) is automatically adapted from the SQL Server schema (`schema.sql`) with these changes:

| SQL Server | SQLite |
|------------|--------|
| `INT IDENTITY(1,1)` | `INTEGER PRIMARY KEY AUTOINCREMENT` |
| `NVARCHAR(n)` | `TEXT` |
| `NVARCHAR(MAX)` | `TEXT` |
| `DECIMAL(18,2)` | `REAL` |
| `GETDATE()` | `CURRENT_TIMESTAMP` |
| `INDEX name (col)` | `CREATE INDEX name ON table(col)` |

## Resetting the Database

To reset your test databases to their initial state:

```bash
cd backend
python init_sqlite.py
```

This will:
1. Delete existing database files
2. Create fresh databases
3. Load the schema
4. Insert sample data

## Custom Database Paths

You can specify custom paths for your SQLite databases:

```bash
# In .env file
SQLITE_CRM_DB_PATH=/path/to/your/crm.db
SQLITE_ERP_DB_PATH=/path/to/your/erp.db
```

Or via environment variables:

```bash
export SQLITE_CRM_DB_PATH=/tmp/test_crm.db
export SQLITE_ERP_DB_PATH=/tmp/test_erp.db
python init_sqlite.py
```

## Testing Workflow

### Development Workflow
```bash
# 1. Initialize test databases
python init_sqlite.py

# 2. Set environment for testing
echo "DB_TYPE=sqlite" > .env

# 3. Run application
python app.py

# 4. Test your changes

# 5. Reset if needed
python init_sqlite.py
```

### CI/CD Pipeline
```bash
# In your CI script
export DB_TYPE=sqlite
export SQLITE_CRM_DB_PATH=ci_crm_test.db
export SQLITE_ERP_DB_PATH=ci_erp_test.db
cd backend
python init_sqlite.py
python app.py &
# Run your tests
```

## Troubleshooting

### Database is locked
SQLite databases can only handle one writer at a time. If you get "database is locked" errors:
- Make sure no other process is accessing the database
- Close any database browser tools (DB Browser for SQLite, etc.)
- Restart the application

### Changes not appearing
If your changes aren't reflected:
```bash
# Reset the database
python init_sqlite.py
```

### Schema errors
If you get schema-related errors, make sure you're using the SQLite schema:
```bash
# Use schema_sqlite.sql, not schema.sql
python init_sqlite.py
```

## Viewing SQLite Databases

You can inspect your SQLite databases using various tools:

### Command Line
```bash
sqlite3 crm_test.db
sqlite> .tables
sqlite> .schema tasks
sqlite> SELECT * FROM tasks;
sqlite> .quit
```

### GUI Tools
- [DB Browser for SQLite](https://sqlitebrowser.org/) (Free, cross-platform)
- [SQLiteStudio](https://sqlitestudio.pl/) (Free, cross-platform)
- VS Code extension: SQLite Viewer

## Production Deployment

**Important**: SQLite is **only for testing**. For production:

1. Use SQL Server (set `DB_TYPE=sqlserver`)
2. Configure proper connection strings
3. Use the SQL Server schema (`schema.sql`)
4. Ensure proper backups and security

## API Compatibility

All API endpoints work identically with both SQLite and SQL Server:
- ✅ Tasks CRUD operations
- ✅ KPIs management
- ✅ Targets tracking
- ✅ ERP data access (customers, sales)
- ✅ Analytics and reporting

## Summary

SQLite support makes testing and development much easier:

| Scenario | Database | Configuration |
|----------|----------|---------------|
| **Local Development** | SQLite | `DB_TYPE=sqlite` |
| **Testing/CI** | SQLite | `DB_TYPE=sqlite` |
| **Staging** | SQL Server | `DB_TYPE=sqlserver` |
| **Production** | SQL Server | `DB_TYPE=sqlserver` |

Simply change the `DB_TYPE` environment variable to switch between databases!
