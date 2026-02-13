import React, { useState, useEffect } from 'react';
import { kpisAPI, targetsAPI, tasksAPI, erpAPI } from '../services/api';
import KPICard from '../components/KPICard';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AlertCircle, CheckCircle, Clock, TrendingUp } from 'lucide-react';

function Dashboard() {
  const [kpis, setKpis] = useState([]);
  const [targets, setTargets] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [salesSummary, setSalesSummary] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError('');
      
      const [kpisRes, targetsRes, tasksRes, salesRes] = await Promise.all([
        kpisAPI.getAll().catch(() => ({ data: { data: [] } })),
        targetsAPI.getAll().catch(() => ({ data: { data: [] } })),
        tasksAPI.getAll({ status: 'pending' }).catch(() => ({ data: { data: [] } })),
        erpAPI.getSalesSummary({ period: 'monthly' }).catch(() => ({ data: { data: [] } }))
      ]);

      setKpis(kpisRes.data.data || []);
      setTargets(targetsRes.data.data || []);
      setTasks(tasksRes.data.data || []);
      setSalesSummary(salesRes.data.data || []);
    } catch (err) {
      setError('Failed to load dashboard data. Please check your database connection.');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  const upcomingTasks = tasks.slice(0, 5);
  const activeTargets = targets.filter(t => t.status === 'active').slice(0, 3);

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="container">
      <h1 style={{ marginBottom: '30px', fontSize: '32px', color: '#333' }}>Dashboard</h1>
      
      {error && (
        <div className="error">
          <AlertCircle size={18} style={{ marginRight: '8px' }} />
          {error}
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-4" style={{ marginBottom: '30px' }}>
        {kpis.length > 0 ? (
          kpis.slice(0, 4).map(kpi => (
            <KPICard key={kpi.id} kpi={kpi} />
          ))
        ) : (
          <div className="card">
            <p>No KPIs configured yet. Go to the KPIs page to create some.</p>
          </div>
        )}
      </div>

      <div className="grid grid-2">
        {/* Sales Trend Chart */}
        <div className="card">
          <h2 style={{ marginBottom: '20px', fontSize: '20px' }}>
            <TrendingUp size={20} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
            Sales Trend
          </h2>
          {salesSummary.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={salesSummary}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="period" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="total_amount" stroke="#007bff" name="Sales" />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <p style={{ textAlign: 'center', color: '#666', padding: '40px' }}>
              No sales data available
            </p>
          )}
        </div>

        {/* Active Targets */}
        <div className="card">
          <h2 style={{ marginBottom: '20px', fontSize: '20px' }}>
            <CheckCircle size={20} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
            Active Targets
          </h2>
          {activeTargets.length > 0 ? (
            <div>
              {activeTargets.map(target => (
                <div key={target.id} style={{ marginBottom: '20px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <strong>{target.name}</strong>
                    <span>{target.progress_percentage}%</span>
                  </div>
                  <div style={{ 
                    width: '100%', 
                    height: '8px', 
                    backgroundColor: '#e0e0e0', 
                    borderRadius: '4px',
                    overflow: 'hidden'
                  }}>
                    <div style={{
                      width: `${Math.min(target.progress_percentage, 100)}%`,
                      height: '100%',
                      backgroundColor: target.progress_percentage >= 100 ? '#28a745' : '#007bff',
                      transition: 'width 0.3s'
                    }} />
                  </div>
                  <div style={{ marginTop: '4px', fontSize: '12px', color: '#666' }}>
                    {target.current_value.toLocaleString()} / {target.target_value.toLocaleString()}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p style={{ textAlign: 'center', color: '#666', padding: '40px' }}>
              No active targets
            </p>
          )}
        </div>
      </div>

      {/* Upcoming Tasks */}
      <div className="card" style={{ marginTop: '20px' }}>
        <h2 style={{ marginBottom: '20px', fontSize: '20px' }}>
          <Clock size={20} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
          Upcoming Tasks
        </h2>
        {upcomingTasks.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Due Date</th>
                <th>Priority</th>
                <th>Assigned To</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {upcomingTasks.map(task => (
                <tr key={task.id}>
                  <td>{task.title}</td>
                  <td>{task.due_date ? new Date(task.due_date).toLocaleDateString() : 'N/A'}</td>
                  <td>
                    <span className={`status-badge status-${
                      task.priority === 'urgent' ? 'red' : 
                      task.priority === 'high' ? 'yellow' : 'blue'
                    }`}>
                      {task.priority}
                    </span>
                  </td>
                  <td>{task.assigned_to || 'Unassigned'}</td>
                  <td>
                    <span className={`status-badge status-${
                      task.status === 'completed' ? 'green' : 'yellow'
                    }`}>
                      {task.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p style={{ textAlign: 'center', color: '#666', padding: '40px' }}>
            No pending tasks
          </p>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
