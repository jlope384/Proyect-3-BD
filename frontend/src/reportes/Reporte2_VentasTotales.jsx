import React, { useEffect, useState } from "react";

export default function Reporte2_VentasTotales() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("/api/reportes/ventas-totales")
      .then((res) => res.json())
      .then((data) => setData(data));
  }, []);

  return (
    <div>
      <h2>Ventas Totales</h2>
      <table>
        <thead>
          <tr>
            <th>Evento</th>
            <th>Tipo de Entrada</th>
            <th>Medio de Pago</th>
            <th>Cantidad</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          {data.map((fila, i) => (
            <tr key={i}>
              <td>{fila.evento}</td>
              <td>{fila.tipo_entrada}</td>
              <td>{fila.medio_pago}</td>
              <td>{fila.cantidad}</td>
              <td>Q{fila.total}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
