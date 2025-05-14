import { useEffect, useState } from 'react';
import axios from 'axios';
import '../index.css';

const StatCard = ({ title, value, unit = '', isLoading = false }) => (
  <div className={`stat-card ${isLoading ? 'loading' : ''}`}>
    <h3 className="stat-title">{title}</h3>
    <div className="stat-value">
      {!isLoading ? (
        <>
          {value}
          {unit && <span className="unit">{unit}</span>}
        </>
      ) : (
        <div className="loading-shimmer"></div>
      )}
    </div>
  </div>
);

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalEventos: 0,
    totalAsistentes: 0,
    promedioAsistencia: 0,
    calificacionPromedio: 0,
    totalRecaudado: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchDashboardStats = async (cancelToken) => {
    try {
      const { data } = await axios.get('http://localhost:8000/api/dashboard', {
        cancelToken,
        timeout: 8000,
        validateStatus: (status) => status < 500
      });

      if (!data || data.status !== 'success') {
        throw new Error(
          data?.detail?.message || 
          data?.message || 
          'Estructura de respuesta inválida'
        );
      }

      if (!data.data) {
        throw new Error('Datos estadísticos no disponibles');
      }

      setStats({
        totalEventos: data.data.totalEventos || 0,
        totalAsistentes: data.data.totalAsistentes || 0,
        promedioAsistencia: data.data.promedioAsistencia || 0,
        calificacionPromedio: data.data.calificacionPromedio || 0,
        totalRecaudado: data.data.totalRecaudado || 0
      });

      setLastUpdated(new Date());
      setError(null);
    } catch (err) {
      if (!axios.isCancel(err)) {
        setError(err.message || 'Error al cargar estadísticas');
        console.error('Error en dashboard:', {
          error: err,
          response: err.response?.data
        });
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const source = axios.CancelToken.source();
    
    fetchDashboardStats(source.token);

    // Auto-refresh cada 30 segundos
    const intervalId = setInterval(() => {
      fetchDashboardStats(source.token);
    }, 30000);

    return () => {
      source.cancel('Componente desmontado');
      clearInterval(intervalId);
    };
  }, []);

  const handleRetry = () => {
    setLoading(true);
    setError(null);
    fetchDashboardStats(axios.CancelToken.source().token);
  };

  if (error) {
    return (
      <div className="dashboard-error">
        <div className="error-content">
          <h2>Error en el Dashboard</h2>
          <p>{error}</p>
          <button 
            onClick={handleRetry}
            className="retry-button"
            disabled={loading}
          >
            {loading ? 'Cargando...' : 'Reintentar'}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Panel de Control</h1>
        {lastUpdated && (
          <p className="last-updated">
            Última actualización: {lastUpdated.toLocaleTimeString()}
          </p>
        )}
      </header>

      <div className="stats-grid">
        <StatCard
          title="Total de Eventos"
          value={stats.totalEventos.toLocaleString()}
          isLoading={loading}
        />
        
        <StatCard
          title="Asistentes Únicos"
          value={stats.totalAsistentes.toLocaleString()}
          isLoading={loading}
        />
        
        <StatCard
          title="Promedio Asistencia"
          value={stats.promedioAsistencia.toFixed(2)}
          unit="personas/evento"
          isLoading={loading}
        />
        
        <StatCard
          title="Calificación Promedio"
          value={stats.calificacionPromedio.toFixed(1)}
          unit="/5"
          isLoading={loading}
        />
        
        <StatCard
          title="Total Recaudado"
          value={stats.totalRecaudado.toLocaleString('en-US', {
            style: 'currency',
            currency: 'GTQ'
          })}
          isLoading={loading}
        />
      </div>
    </div>
  );
};

export default Dashboard;