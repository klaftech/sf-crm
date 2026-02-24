import os
import sqlite3
import pymysql
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


def row_to_dict(row):
    """Convert database row to dictionary
    
    Works with both pymysql.DictCursor, pyodbc.Row and sqlite3.Row objects.
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
    
    Handles both datetime objects (from Azure SQL Database) and strings (from SQLite).
    """
    if value is None:
        return None
    
    # If it's already a string, return it (SQLite case)
    if isinstance(value, str):
        return value
    
    # If it's a datetime object, convert to ISO format (Azure SQL Database case)
    if isinstance(value, datetime):
        return value.isoformat()
    
    # Fallback
    return str(value)


class DatabaseConfig:
    """Database configuration for ERP and CRM databases
    
    Supports MySQL Database (production) and SQLite (testing).
    Set DB_TYPE environment variable to 'sqlite' for testing or 'mysql' for production.
    """
    
    # Database Type Selection
    DB_TYPE = os.getenv('DB_TYPE', 'sqlite').lower()  # 'mysql' or 'sqlite'
    
    # SQLite Configuration (for testing)
    SQLITE_CRM_DB_PATH = os.getenv('SQLITE_CRM_DB_PATH', 'crm_test.db')
    SQLITE_ERP_DB_PATH = os.getenv('SQLITE_ERP_DB_PATH', 'erp_test.db')
    
    # MySQL Database Configuration (for production)
    # ERP Database (Read-Only)
    ERP_DB_SERVER = os.getenv('ERP_DB_SERVER', '')
    ERP_DB_PORT = int(os.getenv('ERP_DB_PORT', 3306))
    ERP_DB_NAME = os.getenv('ERP_DB_NAME', '')
    ERP_DB_USERNAME = os.getenv('ERP_DB_USERNAME', '')
    ERP_DB_PASSWORD = os.getenv('ERP_DB_PASSWORD', '')
    ERP_DB_SSL_CA = os.getenv('ERP_DB_SSL_CA', None)  # Path to CA certificate for SSL
    
    # CRM Database
    CRM_DB_SERVER = os.getenv('CRM_DB_SERVER', '')
    CRM_DB_PORT = int(os.getenv('CRM_DB_PORT', 3306))
    CRM_DB_NAME = os.getenv('CRM_DB_NAME', '')
    CRM_DB_USERNAME = os.getenv('CRM_DB_USERNAME', '')
    CRM_DB_PASSWORD = os.getenv('CRM_DB_PASSWORD', '')
    CRM_DB_SSL_CA = os.getenv('CRM_DB_SSL_CA', None)  # Path to CA certificate for SSL
    
    @staticmethod
    def get_erp_connection():
        """Get connection to ERP database (read-only)
        
        Returns SQLite or MySQL Database connection based on DB_TYPE setting.
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
            # MySQL Database connection
            try:
                ssl_config = None
                if DatabaseConfig.ERP_DB_SSL_CA:
                    ssl_config = {'ca': DatabaseConfig.ERP_DB_SSL_CA}
                
                connection = pymysql.connect(
                    host=DatabaseConfig.ERP_DB_SERVER,
                    port=DatabaseConfig.ERP_DB_PORT,
                    user=DatabaseConfig.ERP_DB_USERNAME,
                    password=DatabaseConfig.ERP_DB_PASSWORD,
                    database=DatabaseConfig.ERP_DB_NAME,
                    cursorclass=pymysql.cursors.DictCursor,
                    connect_timeout=10,
                    read_timeout=300,
                    write_timeout=300,
                    autocommit=True,
                    charset='utf8mb4',
                    ssl=ssl_config,
                    ssl_disabled=ssl_config is None
                )
                return connection
            except pymysql.Error as e:
                print(f"Error connecting to ERP database: {e}")
                raise
    
    @staticmethod
    def get_crm_connection():
        """Get connection to CRM database
        
        Returns SQLite or MySQL Database connection based on DB_TYPE setting.
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
            # MySQL Database connection
            try:
                ssl_config = None
                if DatabaseConfig.CRM_DB_SSL_CA:
                    ssl_config = {'ca': DatabaseConfig.CRM_DB_SSL_CA}
                
                connection = pymysql.connect(
                    host=DatabaseConfig.CRM_DB_SERVER,
                    port=DatabaseConfig.CRM_DB_PORT,
                    user=DatabaseConfig.CRM_DB_USERNAME,
                    password=DatabaseConfig.CRM_DB_PASSWORD,
                    database=DatabaseConfig.CRM_DB_NAME,
                    cursorclass=pymysql.cursors.DictCursor,
                    connect_timeout=10,
                    read_timeout=300,
                    write_timeout=300,
                    autocommit=True,
                    charset='utf8mb4',
                    ssl=ssl_config,
                    ssl_disabled=ssl_config is None
                )
                return connection
            except pymysql.Error as e:
                print(f"Error connecting to CRM database: {e}")
                raise
