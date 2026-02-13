import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

function KPICard({ kpi }) {
  const getStatusColor = (status) => {
    switch (status) {
      case 'green': return '#28a745';
      case 'yellow': return '#ffc107';
      case 'red': return '#dc3545';
      default: return '#6c757d';
    }
  };

  return (
    <div className="card" style={{ 
      borderLeft: `4px solid ${getStatusColor(kpi.status)}`,
      position: 'relative'
    }}>
      <div style={{ marginBottom: '10px', fontSize: '14px', color: '#666', fontWeight: '500' }}>
        {kpi.name}
      </div>
      <div style={{ fontSize: '32px', fontWeight: '700', color: '#333', marginBottom: '10px' }}>
        {kpi.current_value.toLocaleString()}
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ fontSize: '12px', color: '#666' }}>
          Target: {kpi.target_value.toLocaleString()}
        </div>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '4px',
          color: kpi.performance_percentage >= 100 ? '#28a745' : '#dc3545'
        }}>
          {kpi.performance_percentage >= 100 ? (
            <TrendingUp size={16} />
          ) : (
            <TrendingDown size={16} />
          )}
          <span style={{ fontWeight: '600', fontSize: '14px' }}>
            {kpi.performance_percentage}%
          </span>
        </div>
      </div>
      <div style={{ 
        marginTop: '10px',
        padding: '4px 8px',
        borderRadius: '4px',
        fontSize: '11px',
        backgroundColor: '#f8f9fa',
        color: '#666',
        textAlign: 'center'
      }}>
        {kpi.period}
      </div>
    </div>
  );
}

export default KPICard;
