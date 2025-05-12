// src/components/Dashboard.jsx
import React, { useEffect, useState } from 'react';
import { getDashboardStats } from '../services/reportService';
import '../styles/dashboard.css';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getDashboardStats()
      .then(data => {
        setStats(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching dashboard stats:', err);
        setError('Error cargando estadísticas');
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Cargando estadísticas...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      <div className="dashboard__grid">
        <div className="card">
          <h3>Total de Eventos</h3>
          <p>{stats.totalEventos}</p>
        </div>
        <div className="card">
          <h3>Total de Asistentes</h3>
          <p>{stats.totalAsistentes}</p>
        </div>
        <div className="card">
          <h3>Promedio Asistencia</h3>
          <p>{stats.promedioAsistencia.toFixed(2)}</p>
        </div>
        <div className="card">
          <h3>Calificación Promedio</h3>
          <p>{stats.calificacionPromedio.toFixed(2)}</p>
        </div>
        <div className="card">
          <h3>Total Recaudado</h3>
          <p>Q {stats.totalRecaudado.toFixed(2)}</p>
        </div>
      </div>
    </div>
  );
}
