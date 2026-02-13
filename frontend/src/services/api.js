import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Tasks API
export const tasksAPI = {
  getAll: (params = {}) => api.get('/tasks', { params }),
  getById: (id) => api.get(`/tasks/${id}`),
  create: (data) => api.post('/tasks', data),
  update: (id, data) => api.put(`/tasks/${id}`, data),
  delete: (id) => api.delete(`/tasks/${id}`),
};

// KPIs API
export const kpisAPI = {
  getAll: () => api.get('/kpis'),
  getById: (id) => api.get(`/kpis/${id}`),
  create: (data) => api.post('/kpis', data),
  update: (id, data) => api.put(`/kpis/${id}`, data),
  delete: (id) => api.delete(`/kpis/${id}`),
};

// Targets API
export const targetsAPI = {
  getAll: () => api.get('/targets'),
  getById: (id) => api.get(`/targets/${id}`),
  create: (data) => api.post('/targets', data),
  update: (id, data) => api.put(`/targets/${id}`, data),
  delete: (id) => api.delete(`/targets/${id}`),
};

// ERP API
export const erpAPI = {
  getCustomers: (params = {}) => api.get('/erp/customers', { params }),
  getCustomerById: (id) => api.get(`/erp/customers/${id}`),
  getSales: (params = {}) => api.get('/erp/sales', { params }),
  getSalesSummary: (params = {}) => api.get('/erp/sales/summary', { params }),
};

export default api;
