// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 5000,              // opcional: timeout de 5s
});

// Interceptores (opcional) para logging o manejo de errores global
api.interceptors.request.use(cfg => {
  console.log(`[API]→ ${cfg.method.toUpperCase()} ${cfg.url}`, cfg.params || cfg.data);
  return cfg;
});
api.interceptors.response.use(
  res => res,
  err => {
    console.error('[API][ERROR]', err.response?.status, err.response?.data);
    return Promise.reject(err);
  }
);

export default api;
