import React, { useEffect, useState } from "react";

export default function Reporte5_AsistenciaPorCiudad() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("/api/reportes/asistencia-por-ciudad")
      .then((res) => res.json())
      .then((data) => setData(data));
  }, []);

  return (
    <div>
      <h2>Asistencia por Ciudad</h2>
      <table>
        <thead>
          <tr>
            <th>Ciudad</th>
            <th>País</th>
            <th>Asistentes Únicos</th>
            <th>Total Asistencias</th>
          </tr>
        </thead>
        <tbody>
          {data.map((fila, i) => (
            <tr key={i}>
              <td>{fila.ciudad}</td>
              <td>{fila.pais}</td>
              <td>{fila.asistentes_unicos}</td>
              <td>{fila.total_asistencias}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
