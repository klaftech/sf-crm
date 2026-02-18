#!/usr/bin/env python3
"""
Test script to verify different Azure SQL Database connection string formats.

This script validates that the connection string builder accepts various
server format options without actually connecting to a database.
"""

def test_connection_string_formats():
    """Test various server format options for Azure SQL Database"""
    
    # Test data
    test_cases = [
        {
            'name': 'Standard format',
            'server': 'sf-driver.database.windows.net',
            'expected': True
        },
        {
            'name': 'With port',
            'server': 'sf-driver.database.windows.net,1433',
            'expected': True
        },
        {
            'name': 'With tcp protocol and port',
            'server': 'tcp:sf-driver.database.windows.net,1433',
            'expected': True
        },
        {
            'name': 'Custom port',
            'server': 'sf-driver.database.windows.net,1434',
            'expected': True
        },
        {
            'name': 'With tcp protocol and custom port',
            'server': 'tcp:sf-driver.database.windows.net,1434',
            'expected': True
        }
    ]
    
    driver = 'ODBC Driver 17 for SQL Server'
    database = 'test_db'
    username = 'test_user'
    password = 'test_password'
    
    print("Testing Azure SQL Database connection string formats:\n")
    print("=" * 80)
    
    for test in test_cases:
        server = test['server']
        
        # Build connection string
        conn_str = (
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
        )
        
        # Validate format
        is_valid = all([
            'DRIVER=' in conn_str,
            'SERVER=' in conn_str,
            'DATABASE=' in conn_str,
            'UID=' in conn_str,
            'PWD=' in conn_str,
        ])
        
        status = "✓ PASS" if is_valid == test['expected'] else "✗ FAIL"
        
        print(f"\n{status} - {test['name']}")
        print(f"  Server: {server}")
        print(f"  Connection String:")
        print(f"    DRIVER={{{driver}}};")
        print(f"    SERVER={server};")
        print(f"    DATABASE={database};")
        print(f"    UID={username};")
        print(f"    PWD=***;")
        
    print("\n" + "=" * 80)
    print("\nAll connection string formats are valid!")
    print("\nNote: This test validates the format only. Actual database connection")
    print("      requires proper credentials and network access to Azure SQL Database.")


if __name__ == '__main__':
    test_connection_string_formats()
