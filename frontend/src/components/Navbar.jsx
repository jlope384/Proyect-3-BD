// frontend/src/components/Navbar.jsx
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav style={{
      background: '#f0f0f0',
      padding: '1rem',
      marginBottom: '1rem',
      display: 'flex',
      gap: '1rem'
    }}>
      <Link to="/">Dashboard</Link>
      <Link to="/eventos">Eventos</Link>
      <Link to="/reportes">Reportes</Link>
      <Link to="/asistentes">Asistentes</Link>
    </nav>
  );
};

export default Navbar;