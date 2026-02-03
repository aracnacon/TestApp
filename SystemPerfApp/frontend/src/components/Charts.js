import React from 'react';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import './Charts.css';

const Charts = ({ metrics, latest }) => {
  // Prepare data for charts - take last 50 points for performance
  const chartData = metrics
    .slice(0, 50)
    .reverse()
    .map(metric => ({
      time: new Date(metric.timestamp).toLocaleTimeString(),
      cpu: metric.cpu_percent,
      memory: metric.memory_percent,
      timestamp: metric.timestamp,
    }));

  // Prepare disk usage data
  const diskData = latest?.disk_usage ? Object.entries(latest.disk_usage).map(([device, data]) => ({
    device: device,
    used: data.used,
    free: data.free,
    percent: data.percent,
    total: data.total,
  })) : [];

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <div className="charts-container">
      <div className="chart-section">
        <h2>CPU & Memory Usage Over Time</h2>
        <ResponsiveContainer width="100%" height={300}>
          <AreaChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="time" 
              tick={{ fontSize: 12 }}
              interval="preserveStartEnd"
            />
            <YAxis 
              tick={{ fontSize: 12 }}
              label={{ value: 'Percentage (%)', angle: -90, position: 'insideLeft' }}
            />
            <Tooltip />
            <Legend />
            <Area 
              type="monotone" 
              dataKey="cpu" 
              stroke="#3b82f6" 
              fill="#3b82f6" 
              fillOpacity={0.6}
              name="CPU %"
            />
            <Area 
              type="monotone" 
              dataKey="memory" 
              stroke="#10b981" 
              fill="#10b981" 
              fillOpacity={0.6}
              name="Memory %"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-section">
        <h2>CPU Usage Trend</h2>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="time" 
              tick={{ fontSize: 12 }}
              interval="preserveStartEnd"
            />
            <YAxis 
              tick={{ fontSize: 12 }}
              label={{ value: 'CPU %', angle: -90, position: 'insideLeft' }}
            />
            <Tooltip />
            <Line 
              type="monotone" 
              dataKey="cpu" 
              stroke="#3b82f6" 
              strokeWidth={2}
              dot={false}
              name="CPU %"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {diskData.length > 0 && (
        <div className="chart-section">
          <h2>Disk Usage by Drive</h2>
          <div className="disk-usage-grid">
            {diskData.map((disk) => (
              <div key={disk.device} className="disk-card">
                <div className="disk-header">
                  <h3>{disk.device}</h3>
                  <span className="disk-percent">{disk.percent.toFixed(1)}%</span>
                </div>
                <div className="disk-bar">
                  <div 
                    className="disk-bar-fill" 
                    style={{ 
                      width: `${disk.percent}%`,
                      backgroundColor: disk.percent > 80 ? '#ef4444' : disk.percent > 60 ? '#f59e0b' : '#10b981'
                    }}
                  />
                </div>
                <div className="disk-details">
                  <span>Used: {formatBytes(disk.used)}</span>
                  <span>Free: {formatBytes(disk.free)}</span>
                  <span>Total: {formatBytes(disk.total)}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Charts;
