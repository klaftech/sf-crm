import React, { useState, useEffect } from 'react';
import { erpAPI } from '../services/api';
import { BarChart3, TrendingUp } from 'lucide-react';
import { 
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';

function Analytics() {
  const [salesSummary, setSalesSummary] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [period, setPeriod] = useState('monthly');

  useEffect(() => {
    loadAnalytics();
  }, [period]);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await erpAPI.getSalesSummary({ period });
      setSalesSummary(response.data.data || []);
    } catch (err) {
      setError('Failed to load analytics. Please ensure ERP database is connected.');
      console.error('Analytics error:', err);
      setSalesSummary([]);
    } finally {
      setLoading(false);
    }
  };

  const COLORS = ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6c757d', '#17a2b8'];

  // Calculate totals
  const totalSales = salesSummary.reduce((sum, item) => sum + (item.total_amount || 0), 0);
  const totalTransactions = salesSummary.reduce((sum, item) => sum + (item.transaction_count || 0), 0);
  const avgTransactionValue = totalTransactions > 0 ? totalSales / totalTransactions : 0;

  if (loading) {
    return <div className="loading">Loading analytics...</div>;
  }

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <h1 style={{ fontSize: '32px', color: '#333', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <BarChart3 size={32} />
          Analytics & Reporting
        </h1>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <label style={{ fontWeight: '500' }}>Period:</label>
          <select 
            className="input" 
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            style={{ width: 'auto' }}
          >
            <option value="daily">Daily</option>
            <option value="monthly">Monthly</option>
            <option value="yearly">Yearly</option>
          </select>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {/* Summary Cards */}
      <div className="grid grid-3" style={{ marginBottom: '30px' }}>
        <div className="card" style={{ borderLeft: '4px solid #007bff' }}>
          <div style={{ fontSize: '14px', color: '#666', marginBottom: '8px' }}>Total Sales</div>
          <div style={{ fontSize: '28px', fontWeight: '700', color: '#007bff' }}>
            ${totalSales.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          </div>
        </div>
        <div className="card" style={{ borderLeft: '4px solid #28a745' }}>
          <div style={{ fontSize: '14px', color: '#666', marginBottom: '8px' }}>Total Transactions</div>
          <div style={{ fontSize: '28px', fontWeight: '700', color: '#28a745' }}>
            {totalTransactions.toLocaleString()}
          </div>
        </div>
        <div className="card" style={{ borderLeft: '4px solid #ffc107' }}>
          <div style={{ fontSize: '14px', color: '#666', marginBottom: '8px' }}>Avg Transaction Value</div>
          <div style={{ fontSize: '28px', fontWeight: '700', color: '#ffc107' }}>
            ${avgTransactionValue.toLocaleString(undefined, { maximumFractionDigits: 0 })}
          </div>
        </div>
      </div>

      <div className="grid grid-2">
        {/* Sales Trend - Line Chart */}
        <div className="card">
          <h2 style={{ marginBottom: '20px', fontSize: '20px' }}>
            <TrendingUp size={20} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
            Sales Trend Over Time
          </h2>
          {salesSummary.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={salesSummary}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="period" />
                <YAxis />
                <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="total_amount" 
                  stroke="#007bff" 
                  strokeWidth={2}
                  name="Total Sales" 
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <p style={{ textAlign: 'center', color: '#666', padding: '40px' }}>
              No sales data available
            </p>
          )}
        </div>

        {/* Transaction Volume - Bar Chart */}
        <div className="card">
          <h2 style={{ marginBottom: '20px', fontSize: '20px' }}>
            <BarChart3 size={20} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
            Transaction Volume
          </h2>
          {salesSummary.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={salesSummary}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="period" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="transaction_count" fill="#28a745" name="Transactions" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <p style={{ textAlign: 'center', color: '#666', padding: '40px' }}>
              No transaction data available
            </p>
          )}
        </div>
      </div>

      {/* Average Transaction Value - Bar Chart */}
      <div className="card" style={{ marginTop: '20px' }}>
        <h2 style={{ marginBottom: '20px', fontSize: '20px' }}>
          Average Transaction Value by Period
        </h2>
        {salesSummary.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={salesSummary}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="period" />
              <YAxis />
              <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
              <Legend />
              <Bar dataKey="avg_amount" fill="#ffc107" name="Avg Value" />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <p style={{ textAlign: 'center', color: '#666', padding: '40px' }}>
            No data available
          </p>
        )}
      </div>

      {/* Data Table */}
      <div className="card" style={{ marginTop: '20px' }}>
        <h2 style={{ marginBottom: '20px', fontSize: '20px' }}>
          Detailed Sales Data
        </h2>
        {salesSummary.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Period</th>
                <th>Total Sales</th>
                <th>Transactions</th>
                <th>Avg Value</th>
              </tr>
            </thead>
            <tbody>
              {salesSummary.map((item, index) => (
                <tr key={index}>
                  <td style={{ fontWeight: '500' }}>{item.period}</td>
                  <td>${(item.total_amount || 0).toLocaleString(undefined, { maximumFractionDigits: 2 })}</td>
                  <td>{(item.transaction_count || 0).toLocaleString()}</td>
                  <td>${(item.avg_amount || 0).toLocaleString(undefined, { maximumFractionDigits: 2 })}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
            <BarChart3 size={48} style={{ opacity: 0.3, marginBottom: '10px' }} />
            <p>No sales data available for the selected period.</p>
            <p style={{ fontSize: '14px', marginTop: '10px' }}>
              Please ensure your ERP database has sales data in the Sales table.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Analytics;
