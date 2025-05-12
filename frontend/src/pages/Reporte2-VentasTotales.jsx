// frontend/src/pages/Reporte2-VentasTotales.jsx

import React, { useState, useEffect } from 'react';
import ReportFilters from '../components/ReportFilters';
import { getVentasTotales } from '../services/reportService';

export default function Reporte2() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetch = params => {
    setLoading(true);
    getVentasTotales(params)
      .then(res => setData(res))
      .finally(() => setLoading(false));
  };

  useEffect(() => { fetch({}); }, []);

  return (
    <div>
      <h2>Reporte 2 – Ventas Totales por Evento</h2>
      <ReportFilters
        fields={[
          { name: 'fecha_inicio', label: 'Fecha Inicio', type: 'date' },
          { name: 'fecha_fin',    label: 'Fecha Fin',    type: 'date' },
          { name: 'monto_minimo', label: 'Mín. Monto',   type: 'number' },
          { name: 'monto_maximo', label: 'Máx. Monto',   type: 'number' },
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
              <th>Total Recaudado</th>
            </tr>
          </thead>
          <tbody>
            {data.map(r => (
              <tr key={r.evento_id}>
                <td>{r.evento_id}</td>
                <td>{r.evento_nombre}</td>
                <td>
                  {/* Parseamos el valor recibido (número) y formateamos a 2 decimales */}
                  {Number(r.total_recaudado).toFixed(2)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
