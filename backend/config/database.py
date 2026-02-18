import os
import sqlite3
import pyodbc
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


def row_to_dict(row):
    """Convert database row to dictionary
    
    Works with both pyodbc.Row and sqlite3.Row objects.
    """
    if isinstance(row, dict):
        return row
    
    # For sqlite3.Row, use keys() method
    if hasattr(row, 'keys'):
        return {key: row[key] for key in row.keys()}
    
    # For pyodbc.Row, iterate over cursor description
    # This shouldn't normally happen but handle it gracefully
    return {col[0]: getattr(row, col[0]) for col in row.cursor_description}


def format_datetime(value):
    """Format datetime value to ISO format string
    
    Handles both datetime objects (from SQL Server) and strings (from SQLite).
    """
    if value is None:
        return None
    
    # If it's already a string, return it (SQLite case)
    if isinstance(value, str):
        return value
    
    # If it's a datetime object, convert to ISO format (SQL Server case)
    if isinstance(value, datetime):
        return value.isoformat()
    
    # Fallback
    return str(value)


class DatabaseConfig:
    """Database configuration for ERP and CRM databases
    
    Supports both SQL Server/Azure SQL Database (production) and SQLite (testing).
    Set DB_TYPE environment variable to 'sqlite' for testing or 'sqlserver' for production.
    """
    
    # Database Type Selection
    DB_TYPE = os.getenv('DB_TYPE', 'sqlite').lower()  # 'sqlserver' or 'sqlite'
    
    # SQLite Configuration (for testing)
    SQLITE_CRM_DB_PATH = os.getenv('SQLITE_CRM_DB_PATH', 'crm_test.db')
    SQLITE_ERP_DB_PATH = os.getenv('SQLITE_ERP_DB_PATH', 'erp_test.db')
    
    # SQL Server Configuration (for production)
    # ERP Database (Read-Only)
    ERP_DB_SERVER = os.getenv('ERP_DB_SERVER', '')
    ERP_DB_NAME = os.getenv('ERP_DB_NAME', '')
    ERP_DB_USERNAME = os.getenv('ERP_DB_USERNAME', '')
    ERP_DB_PASSWORD = os.getenv('ERP_DB_PASSWORD', '')
    ERP_DB_DRIVER = os.getenv('ERP_DB_DRIVER', 'ODBC Driver 17 for SQL Server')
    
    # CRM Database
    CRM_DB_SERVER = os.getenv('CRM_DB_SERVER', '')
    CRM_DB_NAME = os.getenv('CRM_DB_NAME', '')
    CRM_DB_USERNAME = os.getenv('CRM_DB_USERNAME', '')
    CRM_DB_PASSWORD = os.getenv('CRM_DB_PASSWORD', '')
    CRM_DB_DRIVER = os.getenv('CRM_DB_DRIVER', 'ODBC Driver 17 for SQL Server')
    
    @staticmethod
    def get_erp_connection():
        """Get connection to ERP database (read-only)
        
        Returns SQLite or SQL Server connection based on DB_TYPE setting.
        """
        if DatabaseConfig.DB_TYPE == 'sqlite':
            try:
                connection = sqlite3.connect(DatabaseConfig.SQLITE_ERP_DB_PATH)
                connection.row_factory = sqlite3.Row
                return connection
            except sqlite3.Error as e:
                print(f"Error connecting to SQLite ERP database: {e}")
                raise
        else:
            # SQL Server connection
            try:
                conn_str = (
                    f"DRIVER={{{DatabaseConfig.ERP_DB_DRIVER}}};"
                    f"SERVER={DatabaseConfig.ERP_DB_SERVER};"
                    f"DATABASE={DatabaseConfig.ERP_DB_NAME};"
                    f"UID={DatabaseConfig.ERP_DB_USERNAME};"
                    f"PWD={DatabaseConfig.ERP_DB_PASSWORD};"
                )
                connection = pyodbc.connect(conn_str)
                return connection
            except pyodbc.Error as e:
                print(f"Error connecting to ERP database: {e}")
                raise
    
    @staticmethod
    def get_crm_connection():
        """Get connection to CRM database
        
        Returns SQLite or SQL Server connection based on DB_TYPE setting.
        """
        if DatabaseConfig.DB_TYPE == 'sqlite':
            try:
                connection = sqlite3.connect(DatabaseConfig.SQLITE_CRM_DB_PATH)
                connection.row_factory = sqlite3.Row
                return connection
            except sqlite3.Error as e:
                print(f"Error connecting to SQLite CRM database: {e}")
                raise
        else:
            # SQL Server connection
            try:
                conn_str = (
                    f"DRIVER={{{DatabaseConfig.CRM_DB_DRIVER}}};"
                    f"SERVER={DatabaseConfig.CRM_DB_SERVER};"
                    f"DATABASE={DatabaseConfig.CRM_DB_NAME};"
                    f"UID={DatabaseConfig.CRM_DB_USERNAME};"
                    f"PWD={DatabaseConfig.CRM_DB_PASSWORD};"
                )
                connection = pyodbc.connect(conn_str)
                return connection
            except pyodbc.Error as e:
                print(f"Error connecting to CRM database: {e}")
                raise
