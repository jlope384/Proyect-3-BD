// src/pages/Reporte3-ArtistasPopulares.jsx

import React, { useState, useEffect } from 'react';
import ReportFilters from '../components/ReportFilters';
import { getArtistasPopulares } from '../services/reportService';

export default function Reporte3() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetch = params => {
    setLoading(true);
    getArtistasPopulares(params)
      .then(res => setData(res))
      .finally(() => setLoading(false));
  };

  // fetch inicial
  useEffect(() => { fetch({ limite: 10 }); }, []);

  return (
    <div>
      <h2>Reporte 3 – Artistas Populares</h2>
      <ReportFilters
        fields={[
          { name: 'limite',         label: 'Límite',          type: 'number' },
          { name: 'fecha_inicio',   label: 'Fecha Inicio',    type: 'date' },
          { name: 'fecha_fin',      label: 'Fecha Fin',       type: 'date' },
          { name: 'tipo_evento_id', label: 'ID Tipo Evento',  type: 'number' },
        ]}
        onSubmit={fetch}
      />
      {loading ? (
        <p>Cargando...</p>
      ) : (
        <table className="report-table">
          <thead>
            <tr>
              <th>Artista ID</th>
              <th>Nombre</th>
              <th>Total Asistencia</th>
            </tr>
          </thead>
          <tbody>
            {data.map(r => (
              <tr key={r.artista_id}>
                <td>{r.artista_id}</td>
                <td>{r.artista_nombre}</td>
                <td>{r.total_asistencia}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
