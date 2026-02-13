#!/usr/bin/env python3
"""
Quick demonstration of database switching capability

This script shows how easy it is to switch between SQLite and SQL Server
using just the DB_TYPE environment variable.
"""

import os
import sys

def demo_database_switching():
    """Demonstrate switching between database types"""
    
    print("=" * 70)
    print("DATABASE SWITCHING DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Test SQLite
    print("1. Testing with SQLite...")
    print("-" * 70)
    os.environ['DB_TYPE'] = 'sqlite'
    os.environ['SQLITE_CRM_DB_PATH'] = 'crm_test.db'
    os.environ['SQLITE_ERP_DB_PATH'] = 'erp_test.db'
    
    # Reload config module to pick up env changes
    import config.database as db_module
    import importlib
    importlib.reload(db_module)
    from config.database import DatabaseConfig
    
    print(f"   Database Type: {DatabaseConfig.DB_TYPE}")
    print(f"   CRM Database: {DatabaseConfig.SQLITE_CRM_DB_PATH}")
    print(f"   ERP Database: {DatabaseConfig.SQLITE_ERP_DB_PATH}")
    
    try:
        conn = DatabaseConfig.get_crm_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tasks")
        count = cursor.fetchone()[0]
        print(f"   ✓ Connected successfully - Found {count} tasks")
        conn.close()
    except Exception as e:
        print(f"   ✗ Connection failed: {e}")
    
    print()
    
    # Show what SQL Server would look like
    print("2. Configuration for SQL Server (example)...")
    print("-" * 70)
    print("   Database Type: sqlserver")
    print("   CRM Server: your-crm-server.database.windows.net")
    print("   ERP Server: your-erp-server.database.windows.net")
    print("   (Set DB_TYPE=sqlserver in .env to use SQL Server)")
    
    print()
    print("=" * 70)
    print("SWITCHING SUMMARY")
    print("=" * 70)
    print()
    print("To switch databases, just change ONE environment variable:")
    print()
    print("  For Testing (SQLite):")
    print("    DB_TYPE=sqlite")
    print()
    print("  For Production (SQL Server):")
    print("    DB_TYPE=sqlserver")
    print()
    print("That's it! No code changes needed.")
    print("=" * 70)

if __name__ == '__main__':
    # Check if we're in the backend directory
    if not os.path.exists('config'):
        print("Please run this script from the backend directory:")
        print("  cd backend")
        print("  python demo_switching.py")
        sys.exit(1)
    
    demo_database_switching()
