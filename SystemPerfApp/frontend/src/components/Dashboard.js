import React, { useState, useEffect } from 'react';
import { metricsApi } from '../services/api';
import MetricCard from './MetricCard';
import Charts from './Charts';
import './Dashboard.css';

const Dashboard = () => {
  const [latestMetrics, setLatestMetrics] = useState(null);
  const [historicalMetrics, setHistoricalMetrics] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [autoRefresh, setAutoRefresh] = useState(true);

  const fetchData = async () => {
    try {
      setError(null);
      
      // Collect new metrics
      await metricsApi.collectMetrics();
      
      // Fetch latest metrics
      const latestResponse = await metricsApi.getLatestMetrics();
      setLatestMetrics(latestResponse.data);
      
      // Fetch historical data (last 24 hours)
      const historyResponse = await metricsApi.getMetrics(24);
      setHistoricalMetrics(historyResponse.data.results || historyResponse.data);
      
      // Fetch statistics
      const statsResponse = await metricsApi.getStats(24);
      setStats(statsResponse.data);
      
      setLoading(false);
    } catch (err) {
      console.error('Error fetching metrics:', err);
      setError(err.response?.data?.error || err.message || 'Failed to fetch metrics');
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    
    // Auto-refresh every 5 seconds if enabled
    let interval;
    if (autoRefresh) {
      interval = setInterval(fetchData, 5000);
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh]);

  const formatBytes = (bytes) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  if (loading && !latestMetrics) {
    return (
      <div className="dashboard-loading">
        <p>Loading system metrics...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-controls">
        <button onClick={fetchData} className="refresh-button">
          Refresh Now
        </button>
        <label className="auto-refresh-toggle">
          <input
            type="checkbox"
            checked={autoRefresh}
            onChange={(e) => setAutoRefresh(e.target.checked)}
          />
          Auto-refresh (5s)
        </label>
      </div>

      {error && (
        <div className="error-message">
          <p>Error: {error}</p>
        </div>
      )}

      {latestMetrics && (
        <>
          <div className="metrics-grid">
            <MetricCard
              title="CPU Usage"
              value={`${latestMetrics.cpu_percent}%`}
              subtitle="Current CPU utilization"
              color="#3b82f6"
            />
            <MetricCard
              title="Memory Usage"
              value={`${latestMetrics.memory_percent}%`}
              subtitle={`${formatBytes(latestMetrics.memory_used)} / ${formatBytes(latestMetrics.memory_total)}`}
              color="#10b981"
            />
            <MetricCard
              title="Network Sent"
              value={formatBytes(latestMetrics.network_sent)}
              subtitle="Total bytes sent"
              color="#f59e0b"
            />
            <MetricCard
              title="Network Received"
              value={formatBytes(latestMetrics.network_recv)}
              subtitle="Total bytes received"
              color="#ef4444"
            />
          </div>

          {stats && (
            <div className="stats-section">
              <h2>Statistics (Last 24 Hours)</h2>
              <div className="stats-grid">
                <div className="stat-item">
                  <span className="stat-label">CPU Average:</span>
                  <span className="stat-value">{stats.cpu.average}%</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">CPU Max:</span>
                  <span className="stat-value">{stats.cpu.maximum}%</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Memory Average:</span>
                  <span className="stat-value">{stats.memory.average}%</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Memory Max:</span>
                  <span className="stat-value">{stats.memory.maximum}%</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Total Samples:</span>
                  <span className="stat-value">{stats.total_samples}</span>
                </div>
              </div>
            </div>
          )}

          <Charts metrics={historicalMetrics} latest={latestMetrics} />
        </>
      )}
    </div>
  );
};

export default Dashboard;
