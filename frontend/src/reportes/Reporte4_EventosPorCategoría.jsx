import React, { useEffect, useState } from "react";

export default function Reporte4_EventosPorCategoria() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("/api/reportes/eventos-por-categoria")
      .then((res) => res.json())
      .then((data) => setData(data));
  }, []);

  return (
    <div>
      <h2>Eventos por Categoría</h2>
      <table>
        <thead>
          <tr>
            <th>Categoría</th>
            <th>Total Eventos</th>
            <th>Ingresos Totales</th>
          </tr>
        </thead>
        <tbody>
          {data.map((fila, i) => (
            <tr key={i}>
              <td>{fila.categoria}</td>
              <td>{fila.total_eventos}</td>
              <td>Q{fila.ingresos_totales ?? 0}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
