import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const metricsApi = {
  // Collect new metrics
  collectMetrics: () => {
    return api.post('/metrics/collect/');
  },

  // Get all metrics with optional time range
  getMetrics: (hours = null) => {
    const params = hours ? { hours } : {};
    return api.get('/metrics/', { params });
  },

  // Get latest metrics
  getLatestMetrics: () => {
    return api.get('/metrics/latest/');
  },

  // Get statistics
  getStats: (hours = 24) => {
    return api.get('/metrics/stats/', { params: { hours } });
  },
};

export default api;
