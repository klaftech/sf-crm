#!/bin/bash

# CRM Application Setup Script
echo "=========================================="
echo "CRM Application Setup"
echo "=========================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
echo "✓ Python 3 found: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi
echo "✓ Node.js found: $(node --version)"

# Check npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi
echo "✓ npm found: $(npm --version)"

echo ""
echo "=========================================="
echo "Setting up Backend..."
echo "=========================================="

cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy .env.example to .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit backend/.env with your database credentials"
fi

cd ..

echo ""
echo "=========================================="
echo "Setting up Frontend..."
echo "=========================================="

cd frontend

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install

cd ..

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Configure your database credentials in backend/.env"
echo "2. Run the CRM database schema: sqlcmd -S your-server -d crm_database -U user -P password -i backend/schema.sql"
echo "3. Start the backend: cd backend && source venv/bin/activate && python app.py"
echo "4. Start the frontend: cd frontend && npm run dev"
echo ""
echo "Or use Docker:"
echo "docker-compose up"
echo ""
