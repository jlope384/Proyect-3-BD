import React, { useEffect, useState } from "react";

export default function Reporte3_ArtistasPopulares() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("/api/reportes/artistas-populares")
      .then((res) => res.json())
      .then((data) => setData(data));
  }, []);

  return (
    <div>
      <h2>Artistas Populares</h2>
      <table>
        <thead>
          <tr>
            <th>Artista</th>
            <th>Tipo</th>
            <th>Eventos Participados</th>
            <th>Total Asistentes</th>
          </tr>
        </thead>
        <tbody>
          {data.map((artista, i) => (
            <tr key={i}>
              <td>{artista.artista}</td>
              <td>{artista.tipo}</td>
              <td>{artista.eventos_participados}</td>
              <td>{artista.asistentes_totales}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
