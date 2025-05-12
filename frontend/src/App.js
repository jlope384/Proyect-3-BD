// src/App.js
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';

import Reporte1 from './pages/Reporte1-AsistenciaEventos';
import Reporte2 from './pages/Reporte2-VentasTotales';
import Reporte3 from './pages/Reporte3-ArtistasPopulares';
import Reporte4 from './pages/Reporte4-EventosPorCategoria';
import Reporte5 from './pages/Reporte5-AsistenciaPorCiudad';

function App() {
  return (
    <div className="app-wrapper">
      <Navbar />

      <div className="main-layout">
        <Sidebar />

        <main className="content">
          <Routes>
            {/* Redirige la raíz al dashboard */}
            <Route path="/" element={<Navigate to="/dashboard" replace />} />

            {/* Ruta del dashboard */}
            <Route path="/dashboard" element={<Dashboard />} />

            {/* Rutas de reportes */}
            <Route path="/reporte1" element={<Reporte1 />} />
            <Route path="/reporte2" element={<Reporte2 />} />
            <Route path="/reporte3" element={<Reporte3 />} />
            <Route path="/reporte4" element={<Reporte4 />} />
            <Route path="/reporte5" element={<Reporte5 />} />

            {/* 404 por defecto */}
            <Route path="*" element={<h2>Página no encontrada</h2>} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default App;
