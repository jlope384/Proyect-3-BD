// frontend/src/components/TablaMejorada.jsx
import { useState } from 'react';

const TablaMejorada = ({ datos, columnas, onEditar }) => {
  const [filtro, setFiltro] = useState('');

  return (
    <div className="tabla-container">
      <input
        type="text"
        placeholder="Buscar..."
        onChange={(e) => setFiltro(e.target.value)}
        className="input-busqueda"
      />
      <table>
        <thead>
          <tr>
            {columnas.map((col) => (
              <th key={col}>{col}</th>
            ))}
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {datos.filter(item => 
            Object.values(item).some(val => 
              String(val).toLowerCase().includes(filtro.toLowerCase())
            )
          ).map((item) => (
            <tr key={item.id}>
              {columnas.map((col) => (
                <td key={`${item.id}-${col}`}>{item[col]}</td>
              ))}
              <td>
                <button onClick={() => onEditar(item.id)}>Editar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TablaMejorada;
