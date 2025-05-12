// src/pages/Reporte5-AsistenciaPorCiudad.jsx

import React, { useState, useEffect } from 'react';
import ReportFilters from '../components/ReportFilters';
import { getAsistenciaPorCiudad } from '../services/reportService';

export default function Reporte5() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetch = params => {
    setLoading(true);
    getAsistenciaPorCiudad(params)
      .then(res => setData(res))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetch({}); }, []);

  return (
    <div>
      <h2>Reporte 5 – Asistencia por Ciudad</h2>
      <ReportFilters
        fields={[
          { name: 'fecha_inicio',        label: 'Fecha Inicio',      type: 'date' },
          { name: 'fecha_fin',           label: 'Fecha Fin',         type: 'date' },
          { name: 'tipo_evento_id',      label: 'ID Tipo Evento',    type: 'number' },
          { name: 'categoria_evento_id', label: 'ID Categoría Evento', type: 'number' },
        ]}
        onSubmit={fetch}
      />
      {loading ? (
        <p>Cargando...</p>
      ) : (
        <table className="report-table">
          <thead>
            <tr>
              <th>Ciudad ID</th>
              <th>Nombre Ciudad</th>
              <th>Total Asistencia</th>
            </tr>
          </thead>
          <tbody>
            {data.map(r => (
              <tr key={r.ciudad_id}>
                <td>{r.ciudad_id}</td>
                <td>{r.ciudad_nombre}</td>
                <td>{r.total_asistencia}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
