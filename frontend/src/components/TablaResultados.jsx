import { useState } from 'react';

const TablaResultados = ({ datos, columnas, onFiltrar }) => {
  const [filtro, setFiltro] = useState('');

  const handleFiltrar = () => {
    onFiltrar({ busqueda: filtro });
  };

  return (
    <div className="tabla-container">
      <div className="filtros-tabla">
        <input
          type="text"
          placeholder="Buscar..."
          value={filtro}
          onChange={(e) => setFiltro(e.target.value)}
          className="input-busqueda"
        />
        <button onClick={handleFiltrar} className="boton-buscar">
          Buscar
        </button>
      </div>

      <table className="tabla">
        <thead>
          <tr>
            {columnas.map((col) => (
              <th key={col}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {datos.map((item) => (
            <tr key={item.id}>
              {columnas.map((col) => (
                <td key={`${item.id}-${col}`}>{item[col]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default TablaResultados;