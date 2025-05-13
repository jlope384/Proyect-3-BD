// frontend/src/pages/Reportes.jsx
import { Link } from 'react-router-dom';

const Reportes = () => {
  return (
    <div>
      <h1>Reportes</h1>
      <nav>
        <Link to="/reportes/asistencia">Asistencia a Eventos</Link> | 
        <Link to="/reportes/ventas">Ventas Totales</Link>
      </nav>
      {/* Aquí irán los reportes específicos */}
    </div>
  );
};

export default Reportes;