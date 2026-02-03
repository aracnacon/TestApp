import React from 'react';
import './MetricCard.css';

const MetricCard = ({ title, value, subtitle, color }) => {
  return (
    <div className="metric-card" style={{ borderTopColor: color }}>
      <div className="metric-card-header">
        <h3>{title}</h3>
      </div>
      <div className="metric-card-body">
        <div className="metric-value" style={{ color }}>
          {value}
        </div>
        {subtitle && (
          <div className="metric-subtitle">{subtitle}</div>
        )}
      </div>
    </div>
  );
};

export default MetricCard;
