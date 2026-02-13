#!/usr/bin/env python3
"""
Initialize SQLite databases for testing

This script creates and populates SQLite databases for local testing.
Run this script to set up test databases before running the application in SQLite mode.
"""

import sqlite3
import os
import sys

def init_database(db_path, schema_file):
    """Initialize a SQLite database with the given schema"""
    print(f"Initializing database: {db_path}")
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        print(f"  Removing existing database: {db_path}")
        os.remove(db_path)
    
    # Create new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Read and execute schema
    print(f"  Reading schema from: {schema_file}")
    with open(schema_file, 'r') as f:
        schema = f.read()
    
    # Execute schema (SQLite supports multiple statements in executescript)
    print(f"  Executing schema...")
    cursor.executescript(schema)
    
    conn.commit()
    conn.close()
    
    print(f"  ✓ Database initialized successfully: {db_path}")
    
    # Display statistics
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get table counts
    tables = ['tasks', 'kpis', 'targets', 'notes']
    print(f"\n  Database statistics:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"    {table}: {count} rows")
    
    conn.close()

def main():
    """Main function to initialize both CRM and ERP databases"""
    print("=" * 60)
    print("SQLite Database Initialization for CRM Testing")
    print("=" * 60)
    print()
    
    # Get paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    schema_file = os.path.join(script_dir, 'schema_sqlite.sql')
    
    # Default database paths (can be overridden by environment variables)
    crm_db_path = os.getenv('SQLITE_CRM_DB_PATH', 'crm_test.db')
    erp_db_path = os.getenv('SQLITE_ERP_DB_PATH', 'erp_test.db')
    
    # Make paths absolute if they're relative
    if not os.path.isabs(crm_db_path):
        crm_db_path = os.path.join(script_dir, crm_db_path)
    if not os.path.isabs(erp_db_path):
        erp_db_path = os.path.join(script_dir, erp_db_path)
    
    # Check if schema file exists
    if not os.path.exists(schema_file):
        print(f"Error: Schema file not found: {schema_file}")
        sys.exit(1)
    
    # Initialize CRM database
    print("Step 1: Initializing CRM Database")
    print("-" * 60)
    init_database(crm_db_path, schema_file)
    
    print()
    print("Step 2: Creating ERP Database (using same schema)")
    print("-" * 60)
    # For ERP database, we'll use the same schema (it includes ERP tables)
    init_database(erp_db_path, schema_file)
    
    print()
    print("=" * 60)
    print("✓ Initialization Complete!")
    print("=" * 60)
    print()
    print("To use SQLite for testing, set in your .env file:")
    print("  DB_TYPE=sqlite")
    print(f"  SQLITE_CRM_DB_PATH={os.path.basename(crm_db_path)}")
    print(f"  SQLITE_ERP_DB_PATH={os.path.basename(erp_db_path)}")
    print()
    print("Then start your application:")
    print("  python app.py")
    print()

if __name__ == '__main__':
    main()
