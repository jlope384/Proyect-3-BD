// src/pages/Reporte4-EventosPorCategoria.jsx

import React, { useState, useEffect } from 'react';
import ReportFilters from '../components/ReportFilters';
import { getEventosPorCategoria } from '../services/reportService';

export default function Reporte4() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetch = params => {
    setLoading(true);
    getEventosPorCategoria(params)
      .then(res => setData(res))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetch({}); }, []);

  return (
    <div>
      <h2>Reporte 4 – Eventos por Categoría</h2>
      <ReportFilters
        fields={[
          { name: 'fecha_inicio',   label: 'Fecha Inicio',    type: 'date' },
          { name: 'fecha_fin',      label: 'Fecha Fin',       type: 'date' },
          { name: 'tipo_evento_id', label: 'ID Tipo Evento',  type: 'number' },
          { name: 'ciudad_id',      label: 'ID Ciudad',       type: 'number' },
        ]}
        onSubmit={fetch}
      />
      {loading ? (
        <p>Cargando...</p>
      ) : (
        <table className="report-table">
          <thead>
            <tr>
              <th>Categoría ID</th>
              <th>Nombre Categoría</th>
              <th>Total Eventos</th>
            </tr>
          </thead>
          <tbody>
            {data.map(r => (
              <tr key={r.categoria_id}>
                <td>{r.categoria_id}</td>
                <td>{r.categoria_nombre}</td>
                <td>{r.total_eventos}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
