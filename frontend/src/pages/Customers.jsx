import React, { useState, useEffect } from 'react';
import { erpAPI } from '../services/api';
import { Search, Users } from 'lucide-react';

function Customers() {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadCustomers();
  }, []);

  const loadCustomers = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await erpAPI.getCustomers({ limit: 100 });
      setCustomers(response.data.data || []);
    } catch (err) {
      setError('Failed to load customers. Please ensure ERP database is connected.');
      console.error('Customers error:', err);
      setCustomers([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    try {
      setLoading(true);
      const response = await erpAPI.getCustomers({ search: searchTerm, limit: 100 });
      setCustomers(response.data.data || []);
    } catch (err) {
      setError('Search failed');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const filteredCustomers = customers.filter(customer =>
    customer.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    customer.email?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return <div className="loading">Loading customers...</div>;
  }

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
        <h1 style={{ fontSize: '32px', color: '#333', display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Users size={32} />
          Customers
        </h1>
      </div>

      {error && <div className="error">{error}</div>}

      {/* Search Bar */}
      <div className="card" style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', gap: '10px' }}>
          <div style={{ flex: 1, position: 'relative' }}>
            <Search 
              size={18} 
              style={{ 
                position: 'absolute', 
                left: '12px', 
                top: '50%', 
                transform: 'translateY(-50%)',
                color: '#666'
              }} 
            />
            <input
              type="text"
              className="input"
              placeholder="Search customers by name or email..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ paddingLeft: '40px' }}
            />
          </div>
          <button className="btn btn-primary" onClick={handleSearch}>
            Search
          </button>
        </div>
      </div>

      {/* Customers Table */}
      <div className="card">
        <h2 style={{ marginBottom: '20px', fontSize: '20px' }}>
          Customer List ({filteredCustomers.length})
        </h2>
        {filteredCustomers.length > 0 ? (
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>City</th>
                <th>Country</th>
              </tr>
            </thead>
            <tbody>
              {filteredCustomers.map((customer, index) => (
                <tr key={customer.id || `customer-${index}`}>
                  <td>{customer.id || 'N/A'}</td>
                  <td style={{ fontWeight: '500' }}>{customer.name || 'N/A'}</td>
                  <td>{customer.email || 'N/A'}</td>
                  <td>{customer.phone || 'N/A'}</td>
                  <td>{customer.city || 'N/A'}</td>
                  <td>{customer.country || 'N/A'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
            <Users size={48} style={{ opacity: 0.3, marginBottom: '10px' }} />
            <p>No customers found. Please check your ERP database connection.</p>
            <p style={{ fontSize: '14px', marginTop: '10px' }}>
              Make sure the Customers table exists in your ERP database with the expected schema.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Customers;
