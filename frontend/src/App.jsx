import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Dashboard from './pages/Dashboard';
import Customers from './pages/Customers';
import Tasks from './pages/Tasks';
import KPIs from './pages/KPIs';
import Targets from './pages/Targets';
import Analytics from './pages/Analytics';
import { LayoutDashboard, Users, CheckSquare, Target, TrendingUp, BarChart3 } from 'lucide-react';

function App() {
  return (
    <Router>
      <div className="app">
        <nav style={styles.nav}>
          <div style={styles.navBrand}>
            <BarChart3 size={24} />
            <h1 style={styles.brandText}>CRM System</h1>
          </div>
          <ul style={styles.navList}>
            <li style={styles.navItem}>
              <Link to="/" style={styles.navLink}>
                <LayoutDashboard size={18} />
                <span>Dashboard</span>
              </Link>
            </li>
            <li style={styles.navItem}>
              <Link to="/customers" style={styles.navLink}>
                <Users size={18} />
                <span>Customers</span>
              </Link>
            </li>
            <li style={styles.navItem}>
              <Link to="/tasks" style={styles.navLink}>
                <CheckSquare size={18} />
                <span>Tasks</span>
              </Link>
            </li>
            <li style={styles.navItem}>
              <Link to="/kpis" style={styles.navLink}>
                <TrendingUp size={18} />
                <span>KPIs</span>
              </Link>
            </li>
            <li style={styles.navItem}>
              <Link to="/targets" style={styles.navLink}>
                <Target size={18} />
                <span>Targets</span>
              </Link>
            </li>
            <li style={styles.navItem}>
              <Link to="/analytics" style={styles.navLink}>
                <BarChart3 size={18} />
                <span>Analytics</span>
              </Link>
            </li>
          </ul>
        </nav>
        <main style={styles.main}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/customers" element={<Customers />} />
            <Route path="/tasks" element={<Tasks />} />
            <Route path="/kpis" element={<KPIs />} />
            <Route path="/targets" element={<Targets />} />
            <Route path="/analytics" element={<Analytics />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

const styles = {
  nav: {
    backgroundColor: '#1a1a1a',
    color: 'white',
    padding: '0 20px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    height: '60px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  },
  navBrand: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  brandText: {
    fontSize: '20px',
    fontWeight: '600',
  },
  navList: {
    display: 'flex',
    listStyle: 'none',
    gap: '10px',
  },
  navItem: {
    display: 'flex',
  },
  navLink: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    padding: '8px 16px',
    color: 'white',
    textDecoration: 'none',
    borderRadius: '4px',
    transition: 'background-color 0.2s',
  },
  main: {
    minHeight: 'calc(100vh - 60px)',
  },
};

export default App;
