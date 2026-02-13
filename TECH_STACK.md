# Technology Stack Clarification

## Question: Is this Node.js or React?

### Answer: This is a **Full-Stack Application** with Both Technologies

This CRM application uses **different technologies for different parts**:

## Frontend: React + Node.js

- **Framework**: React 18.2.0
- **Build Tool**: Vite 5.0.8
- **Language**: JavaScript/JSX
- **Runtime Required**: Node.js (for development and building)

The frontend is located in the `/frontend` directory and is a **React application**. While React itself is a JavaScript library, it requires **Node.js** to:
- Run the development server (`npm run dev`)
- Install dependencies (`npm install`)
- Build for production (`npm run build`)

### Frontend Dependencies
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-router-dom": "^6.20.0",
  "axios": "^1.6.2",
  "recharts": "^2.10.3",
  "lucide-react": "^0.294.0"
}
```

## Backend: Python (Flask)

- **Framework**: Flask 3.0.0
- **Language**: Python
- **Runtime Required**: Python 3.8+
- **NOT Node.js**

The backend is located in the `/backend` directory and is a **Python Flask application**. It does NOT use Node.js.

### Backend Dependencies
```
Flask==3.0.0
Flask-CORS==4.0.0
pyodbc==5.0.1
python-dotenv==1.0.0
```

## Architecture Summary

```
┌─────────────────────────────────────────┐
│           Frontend (Port 3000)          │
│                                         │
│  React 18 + Vite                       │
│  Requires: Node.js for dev/build       │
│  Files: /frontend/*                    │
└─────────────────┬───────────────────────┘
                  │
                  │ HTTP/REST API
                  │
┌─────────────────▼───────────────────────┐
│           Backend (Port 5000)           │
│                                         │
│  Python Flask                          │
│  Requires: Python 3.8+                 │
│  Files: /backend/*                     │
└─────────────────┬───────────────────────┘
                  │
                  │
┌─────────────────▼───────────────────────┐
│      Microsoft SQL Server               │
│  ERP Database + CRM Database           │
└─────────────────────────────────────────┘
```

## What You Need to Install

### For Frontend Development:
1. **Node.js** (version 16+)
2. **npm** (comes with Node.js)

```bash
cd frontend
npm install
npm run dev
```

### For Backend Development:
1. **Python** (version 3.8+)
2. **pip** (comes with Python)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Quick Answer

- **Is it React?** ✅ YES - The frontend is React
- **Is it Node.js?** ⚠️ PARTIALLY - Node.js is needed to run/build the React frontend, but the backend is Python, not Node.js
- **Complete Stack**: React (frontend) + Flask/Python (backend) + SQL Server (database)

## Technology Choice Rationale

The problem statement specified:
- **Backend**: Python with Flask framework ✅
- **Frontend**: React ✅
- **Database**: Microsoft SQL Server ✅

This is a **modern full-stack application** that combines:
- React's powerful UI capabilities
- Python/Flask's simplicity and SQL Server integration
- Best-of-breed tools from different ecosystems

## Running the Application

**Option 1: Manual (requires both Node.js and Python)**
```bash
# Terminal 1 - Backend (Python)
cd backend
source venv/bin/activate
python app.py

# Terminal 2 - Frontend (Node.js + React)
cd frontend
npm run dev
```

**Option 2: Docker (requires Docker only)**
```bash
docker-compose up
```

## Summary

This is a **hybrid application**:
- Frontend: **React** (runs on Node.js during development)
- Backend: **Python Flask** (NOT Node.js)
- Together: A complete full-stack CRM system

If you were expecting a pure Node.js backend (like Express.js), this application uses Python/Flask instead, as specified in the original requirements.
