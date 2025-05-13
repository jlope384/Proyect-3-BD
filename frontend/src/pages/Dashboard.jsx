// frontend/src/pages/Dashboard.jsx
import { useEffect, useState } from 'react';
import axios from 'axios';
import '../index.css';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalEventos: 0,
    totalAsistentes: 0,
    promedioAsistencia: 0,
    calificacionPromedio: 0,
    totalRecaudado: 0,
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await axios.get('http://localhost:8000/api/dashboard');
        setStats(res.data);
      } catch (error) {
        console.error('Error al cargar el dashboard:', error);
      }
    };
    fetchStats();
  }, []);

  return (
    <div style={{ padding: '20px' }}>
      <h1 style={{ fontSize: '24px', marginBottom: '20px' }}>Resumen General</h1>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '20px' }}>
        <Card title="Eventos realizados" value={stats.totalEventos} />
        <Card title="Total asistentes" value={stats.totalAsistentes} />
        <Card title="Prom. asistencia por evento" value={stats.promedioAsistencia.toFixed(2)} />
        <Card title="Calificación promedio" value={stats.calificacionPromedio.toFixed(1)} />
        <Card title="Total recaudado (Q)" value={`Q${stats.totalRecaudado.toFixed(2)}`} />
      </div>
    </div>
  );
};

const Card = ({ title, value }) => (
  <div className="card">
    <h2 style={{ color: '#666', fontSize: '14px', marginBottom: '8px' }}>{title}</h2>
    <p style={{ fontSize: '24px', fontWeight: 'bold' }}>{value}</p>
  </div>
);

export default Dashboard;