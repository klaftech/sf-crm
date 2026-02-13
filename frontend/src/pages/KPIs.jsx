import React, { useState, useEffect } from 'react';
import { kpisAPI } from '../services/api';
import { TrendingUp, Plus, Edit2, Trash2 } from 'lucide-react';
import KPICard from '../components/KPICard';

function KPIs() {
  const [kpis, setKpis] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingKPI, setEditingKPI] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    calculation_method: '',
    target_value: '',
    current_value: '',
    period: 'monthly'
  });

  useEffect(() => {
    loadKPIs();
  }, []);

  const loadKPIs = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await kpisAPI.getAll();
      setKpis(response.data.data || []);
    } catch (err) {
      setError('Failed to load KPIs. Please check your CRM database connection.');
      console.error('KPIs error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingKPI) {
        await kpisAPI.update(editingKPI.id, formData);
      } else {
        await kpisAPI.create(formData);
      }
      setShowForm(false);
      setEditingKPI(null);
      setFormData({
        name: '',
        description: '',
        calculation_method: '',
        target_value: '',
        current_value: '',
        period: 'monthly'
      });
      loadKPIs();
    } catch (err) {
      setError('Failed to save KPI');
      console.error('Save error:', err);
    }
  };

  const handleEdit = (kpi) => {
    setEditingKPI(kpi);
    setFormData({
      name: kpi.name,
      description: kpi.description || '',
      calculation_method: kpi.calculation_method || '',
      target_value: kpi.target_value,
      current_value: kpi.current_value,
      period: kpi.period
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this KPI?')) {
      try {
        await kpisAPI.delete(id);
        loadKPIs();
      } catch (err) {
        setError('Failed to delete KPI');
        console.error('Delete error:', err);
      }
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  if (loading) {
    return <div className="loading">Loading KPIs...</div>;
  }

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <h1 style={{ fontSize: '32px', color: '#333', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <TrendingUp size={32} />
          KPI Dashboard
        </h1>
        <button 
          className="btn btn-primary"
          onClick={() => {
            setShowForm(!showForm);
            setEditingKPI(null);
            setFormData({
              name: '',
              description: '',
              calculation_method: '',
              target_value: '',
              current_value: '',
              period: 'monthly'
            });
          }}
        >
          <Plus size={18} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
          New KPI
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {/* KPI Form */}
      {showForm && (
        <div className="card" style={{ marginBottom: '20px' }}>
          <h2 style={{ marginBottom: '20px', fontSize: '20px' }}>
            {editingKPI ? 'Edit KPI' : 'Create New KPI'}
          </h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Name *</label>
              <input
                type="text"
                name="name"
                className="input"
                value={formData.name}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea
                name="description"
                className="input"
                value={formData.description}
                onChange={handleChange}
                rows="2"
              />
            </div>
            <div className="form-group">
              <label>Calculation Method</label>
              <input
                type="text"
                name="calculation_method"
                className="input"
                value={formData.calculation_method}
                onChange={handleChange}
                placeholder="e.g., SUM(sales.amount)"
              />
            </div>
            <div className="grid grid-3">
              <div className="form-group">
                <label>Target Value *</label>
                <input
                  type="number"
                  step="0.01"
                  name="target_value"
                  className="input"
                  value={formData.target_value}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Current Value *</label>
                <input
                  type="number"
                  step="0.01"
                  name="current_value"
                  className="input"
                  value={formData.current_value}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Period</label>
                <select
                  name="period"
                  className="input"
                  value={formData.period}
                  onChange={handleChange}
                >
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                  <option value="quarterly">Quarterly</option>
                  <option value="yearly">Yearly</option>
                </select>
              </div>
            </div>
            <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
              <button type="submit" className="btn btn-primary">
                {editingKPI ? 'Update KPI' : 'Create KPI'}
              </button>
              <button 
                type="button" 
                className="btn btn-secondary"
                onClick={() => {
                  setShowForm(false);
                  setEditingKPI(null);
                }}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-4" style={{ marginBottom: '30px' }}>
        {kpis.map(kpi => (
          <KPICard key={kpi.id} kpi={kpi} />
        ))}
      </div>

      {/* KPI Table */}
      <div className="card">
        <h2 style={{ marginBottom: '20px', fontSize: '20px' }}>
          All KPIs ({kpis.length})
        </h2>
        {kpis.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Current</th>
                <th>Target</th>
                <th>Performance</th>
                <th>Period</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {kpis.map(kpi => (
                <tr key={kpi.id}>
                  <td style={{ fontWeight: '500' }}>{kpi.name}</td>
                  <td>{kpi.current_value.toLocaleString()}</td>
                  <td>{kpi.target_value.toLocaleString()}</td>
                  <td>{kpi.performance_percentage}%</td>
                  <td>{kpi.period}</td>
                  <td>
                    <span className={`status-badge status-${kpi.status}`}>
                      {kpi.status}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <button
                        className="btn btn-secondary"
                        style={{ padding: '6px 12px' }}
                        onClick={() => handleEdit(kpi)}
                      >
                        <Edit2 size={14} />
                      </button>
                      <button
                        className="btn btn-danger"
                        style={{ padding: '6px 12px' }}
                        onClick={() => handleDelete(kpi.id)}
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
            <TrendingUp size={48} style={{ opacity: 0.3, marginBottom: '10px' }} />
            <p>No KPIs found. Create your first KPI to start tracking performance.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default KPIs;
