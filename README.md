# CRM Application with ERP Integration

A comprehensive **full-stack CRM application** with:
- **Backend**: Python Flask (REST API)
- **Frontend**: React 18 + Vite
- **Database**: Microsoft SQL Server / Azure SQL Database (production) / SQLite (testing)

Built for customer relationship management, task tracking, KPI monitoring, and analytics with ERP integration.

> **Note**: This is a **hybrid stack application** - React frontend (requires Node.js for development) + Python Flask backend (NOT Node.js). See [TECH_STACK.md](TECH_STACK.md) for details.

> **Testing**: Want to test without SQL Server? Use **SQLite mode** for local development! See [SQLITE_TESTING.md](SQLITE_TESTING.md) for quick setup.

## Features

- **Dashboard**: Overview of KPIs, targets, and upcoming tasks with visual charts
- **Customer Management**: View and search customers from ERP database
- **Task Management**: Create, track, and manage follow-up tasks
- **KPI Tracking**: Define custom KPIs and monitor performance against targets
- **Target Management**: Set and track various business targets (revenue, customers, etc.)
- **Analytics**: Interactive charts and reports for sales trends and performance metrics

## Technology Stack

### Backend (Python - NOT Node.js)
- **Language**: Python 3.8+
- **Framework**: Flask 3.0 - Web framework
- **Database**: pyodbc - SQL Server connectivity
- **CORS**: Flask-CORS - Cross-origin resource sharing
- **Config**: python-dotenv - Environment variables

### Frontend (React - requires Node.js)
- **Library**: React 18.2
- **Build Tool**: Vite 5.0 - Fast build tool
- **Charts**: Recharts - Data visualization
- **HTTP Client**: Axios - API requests
- **Routing**: React Router 6 - Navigation
- **Icons**: Lucide React - UI icons

### Database
- **Microsoft SQL Server / Azure SQL Database** (production deployment)
- **SQLite** (local testing - no SQL Server required!)
- **ODBC Driver 17** for SQL Server (production only)

See [SQLITE_TESTING.md](SQLITE_TESTING.md) for SQLite setup instructions.

### Development Tools
- **Node.js 16+** - Required for React frontend development
- **Python 3.8+** - Required for Flask backend
- **Docker** - Optional, for containerized deployment

> **Important**: While the frontend uses React (which requires Node.js), the backend is Python/Flask, **NOT** a Node.js server like Express. This is a hybrid stack.

## Project Structure

```
sf-crm/
├── backend/
│   ├── app/
│   │   ├── routes/          # API endpoints
│   │   ├── models/          # Data models
│   │   ├── services/        # Business logic
│   │   └── utils/           # Utility functions
│   ├── config/              # Configuration
│   ├── app.py               # Flask application
│   ├── wsgi.py              # WSGI entry point
│   ├── schema.sql           # CRM database schema
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   ├── App.jsx          # Main app component
│   │   └── main.jsx         # Application entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- **For Production**: Microsoft SQL Server or Azure SQL Database + ODBC Driver 17
- **For Testing**: Nothing extra needed! SQLite is built into Python

## Quick Start with SQLite (Testing)

Want to try the app without setting up SQL Server? Use SQLite mode:

```bash
# 1. Setup backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Initialize SQLite databases
python init_sqlite.py

# 3. Configure for SQLite
echo "DB_TYPE=sqlite" > .env
cat .env.example >> .env

# 4. Run the backend
python app.py

# 5. In another terminal, setup frontend
cd ../frontend
npm install
npm run dev
```

**That's it!** The app is now running with SQLite at http://localhost:3000

For full documentation, see [SQLITE_TESTING.md](SQLITE_TESTING.md)

## Setup Instructions (SQL Server / Azure SQL Database Production)

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Microsoft SQL Server or Azure SQL Database (with ERP database already set up)
- ODBC Driver 17 for SQL Server

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file with your database credentials:
   ```
   # Set DB_TYPE to 'sqlserver' for Azure SQL Database
   DB_TYPE=sqlserver
   
   # ERP Database (Read-Only) - Azure SQL Database
   # Server format: your-server-name.database.windows.net
   # Username format: username (NOT username@servername)
   ERP_DB_SERVER=your-erp-server.database.windows.net
   ERP_DB_NAME=erp_database
   ERP_DB_USERNAME=readonly_user
   ERP_DB_PASSWORD=your-password
   
   # CRM Database - Azure SQL Database
   # Server format: your-server-name.database.windows.net
   # Username format: username (NOT username@servername)
   CRM_DB_SERVER=your-crm-server.database.windows.net
   CRM_DB_NAME=crm_database
   CRM_DB_USERNAME=crm_user
   CRM_DB_PASSWORD=your-password
   
   FLASK_SECRET_KEY=your-secret-key-here
   ```

5. **Set up CRM database:**
   
   Run the `schema.sql` script on your CRM SQL Server database:
   ```bash
   sqlcmd -S your-crm-server -d crm_database -U crm_user -P your-password -i schema.sql
   ```
   
   Or execute the script using SQL Server Management Studio (SSMS).

6. **Run the backend server:**
   ```bash
   python app.py
   ```
   
   The API will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure API endpoint (optional):**
   
   Create a `.env` file in the frontend directory if you need to change the API URL:
   ```
   VITE_API_URL=http://localhost:5000/api
   ```

4. **Run the development server:**
   ```bash
   npm run dev
   ```
   
   The application will be available at `http://localhost:3000`

5. **Build for production:**
   ```bash
   npm run build
   ```
   
   The production files will be in the `dist` directory.

## Database Configuration

### ERP Database Schema

The application expects the following tables in your ERP database (adjust column names in `backend/app/services/erp_service.py` if needed):

- **Customers**: CustomerID, CustomerName, Email, Phone, Address, City, Country
- **Sales**: SaleID, CustomerID, SaleDate, TotalAmount, ProductName, Quantity

### CRM Database Schema

The CRM database tables are created by running `schema.sql`:

- **tasks**: Task management
- **kpis**: KPI definitions and tracking
- **targets**: Target management
- **notes**: Customer notes

## API Documentation

### Base URL: `http://localhost:5000/api`

### Tasks
- `GET /tasks` - Get all tasks (optional: ?status=pending&assigned_to=John)
- `GET /tasks/:id` - Get task by ID
- `POST /tasks` - Create new task
- `PUT /tasks/:id` - Update task
- `DELETE /tasks/:id` - Delete task

### KPIs
- `GET /kpis` - Get all KPIs
- `GET /kpis/:id` - Get KPI by ID
- `POST /kpis` - Create new KPI
- `PUT /kpis/:id` - Update KPI
- `DELETE /kpis/:id` - Delete KPI

### Targets
- `GET /targets` - Get all targets
- `GET /targets/:id` - Get target by ID
- `POST /targets` - Create new target
- `PUT /targets/:id` - Update target
- `DELETE /targets/:id` - Delete target

### ERP Data
- `GET /erp/customers` - Get customers from ERP (optional: ?search=term&limit=100)
- `GET /erp/customers/:id` - Get customer by ID from ERP
- `GET /erp/sales` - Get sales data (optional: ?start_date=&end_date=&customer_id=)
- `GET /erp/sales/summary` - Get sales summary (optional: ?period=monthly)

## Security Considerations

- ERP database connection uses read-only credentials (recommended)
- All sensitive configuration stored in environment variables
- CORS configured for specific frontend origins
- SQL injection prevention through parameterized queries
- No sensitive information exposed in error messages

## Customization

### Adjusting ERP Schema

If your ERP database has different table/column names, update the SQL queries in:
- `backend/app/services/erp_service.py`

### Adding New Features

1. Create model in `backend/app/models/`
2. Create service in `backend/app/services/`
3. Create route in `backend/app/routes/`
4. Register blueprint in `backend/app.py`
5. Create React component in `frontend/src/components/` or `frontend/src/pages/`
6. Add route in `frontend/src/App.jsx`

## Troubleshooting

### Backend Issues

**Connection to SQL Server / Azure SQL Database fails:**
- Verify ODBC Driver 17 for SQL Server is installed
- Check server name, database name, and credentials in `.env`
- For Azure SQL Database:
  - Ensure your IP address is added to the Azure SQL firewall rules
  - Use server format: `your-server-name.database.windows.net`
  - Use username format: `username` (NOT `username@servername`)
  - Verify the database allows SQL Server authentication (not just Azure AD)
- Ensure SQL Server allows remote connections
- Check firewall settings

**Module not found errors:**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

### Frontend Issues

**Cannot connect to API:**
- Verify backend is running on port 5000
- Check CORS configuration in backend
- Verify API_URL in frontend configuration

**Build errors:**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

## Development

### Running Tests

Backend:
```bash
cd backend
python -m pytest
```

Frontend:
```bash
cd frontend
npm test
```

### Code Style

Backend:
```bash
cd backend
black .
flake8 .
```

Frontend:
```bash
cd frontend
npm run lint
```

## Deployment

### Production Deployment

1. **Backend:**
   - Use a production WSGI server (gunicorn, uwsgi)
   - Set `FLASK_ENV=production` in `.env`
   - Use SSL for database connections
   - Set up proper logging

2. **Frontend:**
   - Build production bundle: `npm run build`
   - Serve static files with nginx or similar
   - Configure proper environment variables

3. **Database:**
   - Use separate production database
   - Regular backups
   - Monitor performance

## License

This project is proprietary software. All rights reserved.

## Support

For issues or questions, please contact the development team.
