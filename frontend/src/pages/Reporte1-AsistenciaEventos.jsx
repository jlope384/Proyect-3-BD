// frontend/src/pages/Reporte1-AsistenciaEventos.jsx

import React, { useState, useEffect } from 'react';
import ReportFilters from '../components/ReportFilters';
import { getAsistenciaEventos } from '../services/reportService';

export default function Reporte1() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetch = params => {
    setLoading(true);
    getAsistenciaEventos(params)
      .then(res => setData(res))
      .finally(() => setLoading(false));
  };

  // fetch inicial sin filtros
  useEffect(() => { fetch({}); }, []);

  return (
    <div>
      <h2>Reporte 1 – Asistencia por Evento</h2>
      <ReportFilters
        fields={[
          { name: 'fecha_inicio', label: 'Fecha Inicio', type: 'date' },
          { name: 'fecha_fin',    label: 'Fecha Fin',    type: 'date' },
          { name: 'evento_id',    label: 'ID Evento',    type: 'number' },
          { name: 'ciudad_id',    label: 'ID Ciudad',    type: 'number' },   // 4º filtro no trivial
        ]}
        onSubmit={fetch}
      />
      {loading ? (
        <p>Cargando...</p>
      ) : (
        <table className="report-table">
          <thead>
            <tr>
              <th>Evento ID</th>
              <th>Nombre</th>
              <th>Total Asistentes</th>
            </tr>
          </thead>
          <tbody>
            {data.map(r => (
              <tr key={r.evento_id}>
                <td>{r.evento_id}</td>
                <td>{r.evento_nombre}</td>
                <td>{r.total_asistentes}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
