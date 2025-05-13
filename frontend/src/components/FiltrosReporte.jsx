
import { useState } from 'react';

const FiltrosReporte = ({ onFiltrar }) => {
  const [fechaInicio, setFechaInicio] = useState('');
  const [fechaFin, setFechaFin] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onFiltrar({ fechaInicio, fechaFin });
  };

  return (
    <form onSubmit={handleSubmit} className="filtros-container">
      <div>
        <label>Fecha Inicio:</label>
        <input 
          type="date" 
          value={fechaInicio}
          onChange={(e) => setFechaInicio(e.target.value)}
        />
      </div>
      <div>
        <label>Fecha Fin:</label>
        <input 
          type="date" 
          value={fechaFin}
          onChange={(e) => setFechaFin(e.target.value)}
        />
      </div>
      <button type="submit">Aplicar Filtros</button>
    </form>
  );
};

export default FiltrosReporte;