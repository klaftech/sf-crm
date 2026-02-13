#!/usr/bin/env python3
"""
Environment Check Script
This script verifies that all prerequisites are installed and configured correctly.
"""

import sys
import subprocess
import os

def check_command(command, name, min_version=None):
    """Check if a command exists and optionally verify version"""
    try:
        result = subprocess.run([command, '--version'], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        version = result.stdout.split()[0] if result.stdout else "Unknown"
        print(f"✓ {name} is installed: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"✗ {name} is NOT installed")
        return False

def check_python_packages():
    """Check if required Python packages can be imported"""
    package_imports = {
        'flask': 'flask',
        'flask_cors': 'flask_cors', 
        'pyodbc': 'pyodbc',
        'python-dotenv': 'dotenv'
    }
    all_installed = True
    
    print("\nChecking Python packages...")
    for package, import_name in package_imports.items():
        try:
            __import__(import_name)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            all_installed = False
    
    return all_installed

def check_env_file():
    """Check if .env file exists"""
    env_path = os.path.join('backend', '.env')
    if os.path.exists(env_path):
        print(f"\n✓ .env file exists at {env_path}")
        return True
    else:
        print(f"\n✗ .env file does NOT exist at {env_path}")
        print(f"  Please copy backend/.env.example to backend/.env and configure it")
        return False

def check_node_modules():
    """Check if node_modules exists"""
    node_modules_path = os.path.join('frontend', 'node_modules')
    if os.path.exists(node_modules_path):
        print(f"\n✓ Node modules are installed at {node_modules_path}")
        return True
    else:
        print(f"\n✗ Node modules are NOT installed")
        print(f"  Run 'cd frontend && npm install'")
        return False

def main():
    print("=" * 60)
    print("CRM Application Environment Check")
    print("=" * 60)
    
    print("\nChecking system requirements...")
    python_ok = check_command('python3', 'Python 3')
    node_ok = check_command('node', 'Node.js')
    npm_ok = check_command('npm', 'npm')
    
    print("\nChecking optional tools...")
    check_command('docker', 'Docker')
    check_command('docker-compose', 'Docker Compose')
    
    # Only check Python packages if Python is available
    if python_ok:
        # Check if we're in a virtual environment
        in_venv = hasattr(sys, 'real_prefix') or (
            hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
        )
        
        if in_venv:
            print("\n✓ Running in a virtual environment")
        else:
            print("\n⚠ Not running in a virtual environment")
            print("  Consider activating venv: source backend/venv/bin/activate")
        
        check_python_packages()
    
    env_ok = check_env_file()
    
    if node_ok and npm_ok:
        check_node_modules()
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    if python_ok and node_ok and npm_ok:
        print("✓ All core requirements are installed")
        if not env_ok:
            print("⚠ Configuration needed: Create backend/.env file")
    else:
        print("✗ Some requirements are missing. Please install them.")
        sys.exit(1)
    
    print("\nNext steps:")
    print("1. Configure backend/.env with your database credentials")
    print("2. Run backend/schema.sql on your CRM database")
    print("3. Start backend: cd backend && source venv/bin/activate && python app.py")
    print("4. Start frontend: cd frontend && npm run dev")

if __name__ == '__main__':
    main()
