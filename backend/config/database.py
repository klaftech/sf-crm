import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    """Database configuration for ERP and CRM databases"""
    
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
        """Get connection to ERP database (read-only)"""
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
        """Get connection to CRM database"""
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
