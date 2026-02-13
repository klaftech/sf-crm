import React, { useState, useEffect } from 'react';
import { targetsAPI } from '../services/api';
import { Target, Plus, Edit2, Trash2 } from 'lucide-react';

function Targets() {
  const [targets, setTargets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingTarget, setEditingTarget] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    target_type: 'revenue',
    target_value: '',
    current_value: '',
    start_date: '',
    end_date: '',
    status: 'active'
  });

  useEffect(() => {
    loadTargets();
  }, []);

  const loadTargets = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await targetsAPI.getAll();
      setTargets(response.data.data || []);
    } catch (err) {
      setError('Failed to load targets. Please check your CRM database connection.');
      console.error('Targets error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingTarget) {
        await targetsAPI.update(editingTarget.id, formData);
      } else {
        await targetsAPI.create(formData);
      }
      setShowForm(false);
      setEditingTarget(null);
      setFormData({
        name: '',
        description: '',
        target_type: 'revenue',
        target_value: '',
        current_value: '',
        start_date: '',
        end_date: '',
        status: 'active'
      });
      loadTargets();
    } catch (err) {
      setError('Failed to save target');
      console.error('Save error:', err);
    }
  };

  const handleEdit = (target) => {
    setEditingTarget(target);
    setFormData({
      name: target.name,
      description: target.description || '',
      target_type: target.target_type,
      target_value: target.target_value,
      current_value: target.current_value,
      start_date: target.start_date ? target.start_date.split('T')[0] : '',
      end_date: target.end_date ? target.end_date.split('T')[0] : '',
      status: target.status
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this target?')) {
      try {
        await targetsAPI.delete(id);
        loadTargets();
      } catch (err) {
        setError('Failed to delete target');
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
    return <div className="loading">Loading targets...</div>;
  }

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <h1 style={{ fontSize: '32px', color: '#333', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Target size={32} />
          Target Management
        </h1>
        <button 
          className="btn btn-primary"
          onClick={() => {
            setShowForm(!showForm);
            setEditingTarget(null);
            setFormData({
              name: '',
              description: '',
              target_type: 'revenue',
              target_value: '',
              current_value: '',
              start_date: '',
              end_date: '',
              status: 'active'
            });
          }}
        >
          <Plus size={18} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
          New Target
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {/* Target Form */}
      {showForm && (
        <div className="card" style={{ marginBottom: '20px' }}>
          <h2 style={{ marginBottom: '20px', fontSize: '20px' }}>
            {editingTarget ? 'Edit Target' : 'Create New Target'}
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
            <div className="grid grid-2">
              <div className="form-group">
                <label>Target Type *</label>
                <select
                  name="target_type"
                  className="input"
                  value={formData.target_type}
                  onChange={handleChange}
                  required
                >
                  <option value="revenue">Revenue</option>
                  <option value="units">Units Sold</option>
                  <option value="customers">Customer Acquisition</option>
                  <option value="tasks">Task Completion</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div className="form-group">
                <label>Status</label>
                <select
                  name="status"
                  className="input"
                  value={formData.status}
                  onChange={handleChange}
                >
                  <option value="active">Active</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                  <option value="at_risk">At Risk</option>
                </select>
              </div>
            </div>
            <div className="grid grid-2">
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
                <label>Current Value</label>
                <input
                  type="number"
                  step="0.01"
                  name="current_value"
                  className="input"
                  value={formData.current_value}
                  onChange={handleChange}
                />
              </div>
            </div>
            <div className="grid grid-2">
              <div className="form-group">
                <label>Start Date</label>
                <input
                  type="date"
                  name="start_date"
                  className="input"
                  value={formData.start_date}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label>End Date</label>
                <input
                  type="date"
                  name="end_date"
                  className="input"
                  value={formData.end_date}
                  onChange={handleChange}
                />
              </div>
            </div>
            <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
              <button type="submit" className="btn btn-primary">
                {editingTarget ? 'Update Target' : 'Create Target'}
              </button>
              <button 
                type="button" 
                className="btn btn-secondary"
                onClick={() => {
                  setShowForm(false);
                  setEditingTarget(null);
                }}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Target Cards */}
      <div className="grid grid-3" style={{ marginBottom: '30px' }}>
        {targets.slice(0, 6).map(target => (
          <div key={target.id} className="card" style={{ 
            borderLeft: `4px solid ${
              target.progress_percentage >= 100 ? '#28a745' :
              target.progress_percentage >= 75 ? '#007bff' :
              target.progress_percentage >= 50 ? '#ffc107' : '#dc3545'
            }`
          }}>
            <div style={{ marginBottom: '10px' }}>
              <div style={{ fontSize: '16px', fontWeight: '600', marginBottom: '4px' }}>
                {target.name}
              </div>
              <div style={{ fontSize: '12px', color: '#666' }}>
                {target.target_type}
              </div>
            </div>
            <div style={{ marginBottom: '10px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                <span style={{ fontSize: '12px', color: '#666' }}>Progress</span>
                <span style={{ fontSize: '14px', fontWeight: '600' }}>
                  {target.progress_percentage}%
                </span>
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
            </div>
            <div style={{ fontSize: '12px', color: '#666' }}>
              {target.current_value.toLocaleString()} / {target.target_value.toLocaleString()}
            </div>
            <div style={{ marginTop: '10px' }}>
              <span className={`status-badge status-${
                target.status === 'active' ? 'blue' :
                target.status === 'completed' ? 'green' :
                target.status === 'at_risk' ? 'red' : 'yellow'
              }`}>
                {target.status}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Target Table */}
      <div className="card">
        <h2 style={{ marginBottom: '20px', fontSize: '20px' }}>
          All Targets ({targets.length})
        </h2>
        {targets.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Progress</th>
                <th>End Date</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {targets.map(target => (
                <tr key={target.id}>
                  <td style={{ fontWeight: '500' }}>{target.name}</td>
                  <td>{target.target_type}</td>
                  <td>
                    <div style={{ minWidth: '120px' }}>
                      <div style={{ marginBottom: '4px' }}>
                        {target.progress_percentage}%
                      </div>
                      <div style={{ 
                        width: '100%', 
                        height: '6px', 
                        backgroundColor: '#e0e0e0', 
                        borderRadius: '3px',
                        overflow: 'hidden'
                      }}>
                        <div style={{
                          width: `${Math.min(target.progress_percentage, 100)}%`,
                          height: '100%',
                          backgroundColor: target.progress_percentage >= 100 ? '#28a745' : '#007bff'
                        }} />
                      </div>
                    </div>
                  </td>
                  <td>{target.end_date ? new Date(target.end_date).toLocaleDateString() : 'N/A'}</td>
                  <td>
                    <span className={`status-badge status-${
                      target.status === 'active' ? 'blue' :
                      target.status === 'completed' ? 'green' :
                      target.status === 'at_risk' ? 'red' : 'yellow'
                    }`}>
                      {target.status}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <button
                        className="btn btn-secondary"
                        style={{ padding: '6px 12px' }}
                        onClick={() => handleEdit(target)}
                      >
                        <Edit2 size={14} />
                      </button>
                      <button
                        className="btn btn-danger"
                        style={{ padding: '6px 12px' }}
                        onClick={() => handleDelete(target.id)}
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
            <Target size={48} style={{ opacity: 0.3, marginBottom: '10px' }} />
            <p>No targets found. Create your first target to start tracking goals.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Targets;
