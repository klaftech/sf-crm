import React, { useState, useEffect } from 'react';
import { tasksAPI } from '../services/api';
import { CheckSquare, Plus, Edit2, Trash2 } from 'lucide-react';

function Tasks() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    customer_id: '',
    due_date: '',
    assigned_to: '',
    status: 'pending',
    priority: 'medium'
  });

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await tasksAPI.getAll();
      setTasks(response.data.data || []);
    } catch (err) {
      setError('Failed to load tasks. Please check your CRM database connection.');
      console.error('Tasks error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingTask) {
        await tasksAPI.update(editingTask.id, formData);
      } else {
        await tasksAPI.create(formData);
      }
      setShowForm(false);
      setEditingTask(null);
      setFormData({
        title: '',
        description: '',
        customer_id: '',
        due_date: '',
        assigned_to: '',
        status: 'pending',
        priority: 'medium'
      });
      loadTasks();
    } catch (err) {
      setError('Failed to save task');
      console.error('Save error:', err);
    }
  };

  const handleEdit = (task) => {
    setEditingTask(task);
    setFormData({
      title: task.title,
      description: task.description || '',
      customer_id: task.customer_id || '',
      due_date: task.due_date ? task.due_date.split('T')[0] : '',
      assigned_to: task.assigned_to || '',
      status: task.status,
      priority: task.priority
    });
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      try {
        await tasksAPI.delete(id);
        loadTasks();
      } catch (err) {
        setError('Failed to delete task');
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
    return <div className="loading">Loading tasks...</div>;
  }

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <h1 style={{ fontSize: '32px', color: '#333', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <CheckSquare size={32} />
          Tasks Management
        </h1>
        <button 
          className="btn btn-primary"
          onClick={() => {
            setShowForm(!showForm);
            setEditingTask(null);
            setFormData({
              title: '',
              description: '',
              customer_id: '',
              due_date: '',
              assigned_to: '',
              status: 'pending',
              priority: 'medium'
            });
          }}
        >
          <Plus size={18} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
          New Task
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {/* Task Form */}
      {showForm && (
        <div className="card" style={{ marginBottom: '20px' }}>
          <h2 style={{ marginBottom: '20px', fontSize: '20px' }}>
            {editingTask ? 'Edit Task' : 'Create New Task'}
          </h2>
          <form onSubmit={handleSubmit}>
            <div className="grid grid-2">
              <div className="form-group">
                <label>Title *</label>
                <input
                  type="text"
                  name="title"
                  className="input"
                  value={formData.title}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Customer ID</label>
                <input
                  type="number"
                  name="customer_id"
                  className="input"
                  value={formData.customer_id}
                  onChange={handleChange}
                />
              </div>
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea
                name="description"
                className="input"
                value={formData.description}
                onChange={handleChange}
                rows="3"
              />
            </div>
            <div className="grid grid-2">
              <div className="form-group">
                <label>Due Date</label>
                <input
                  type="date"
                  name="due_date"
                  className="input"
                  value={formData.due_date}
                  onChange={handleChange}
                />
              </div>
              <div className="form-group">
                <label>Assigned To</label>
                <input
                  type="text"
                  name="assigned_to"
                  className="input"
                  value={formData.assigned_to}
                  onChange={handleChange}
                />
              </div>
            </div>
            <div className="grid grid-2">
              <div className="form-group">
                <label>Status</label>
                <select
                  name="status"
                  className="input"
                  value={formData.status}
                  onChange={handleChange}
                >
                  <option value="pending">Pending</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>
              <div className="form-group">
                <label>Priority</label>
                <select
                  name="priority"
                  className="input"
                  value={formData.priority}
                  onChange={handleChange}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="urgent">Urgent</option>
                </select>
              </div>
            </div>
            <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
              <button type="submit" className="btn btn-primary">
                {editingTask ? 'Update Task' : 'Create Task'}
              </button>
              <button 
                type="button" 
                className="btn btn-secondary"
                onClick={() => {
                  setShowForm(false);
                  setEditingTask(null);
                }}
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Tasks List */}
      <div className="card">
        <h2 style={{ marginBottom: '20px', fontSize: '20px' }}>
          All Tasks ({tasks.length})
        </h2>
        {tasks.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Due Date</th>
                <th>Priority</th>
                <th>Assigned To</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {tasks.map(task => (
                <tr key={task.id}>
                  <td style={{ fontWeight: '500' }}>{task.title}</td>
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
                      task.status === 'completed' ? 'green' : 
                      task.status === 'in_progress' ? 'blue' : 'yellow'
                    }`}>
                      {task.status}
                    </span>
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '8px' }}>
                      <button
                        className="btn btn-secondary"
                        style={{ padding: '6px 12px' }}
                        onClick={() => handleEdit(task)}
                      >
                        <Edit2 size={14} />
                      </button>
                      <button
                        className="btn btn-danger"
                        style={{ padding: '6px 12px' }}
                        onClick={() => handleDelete(task.id)}
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
            <CheckSquare size={48} style={{ opacity: 0.3, marginBottom: '10px' }} />
            <p>No tasks found. Create your first task to get started.</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Tasks;
