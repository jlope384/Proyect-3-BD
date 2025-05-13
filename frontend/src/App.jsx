// frontend/src/App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Reportes from './pages/Reportes';
import Eventos from './pages/Eventos';
import Asistentes from './pages/Asistentes';
import Navbar from './components/Navbar';

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/reportes" element={<Reportes />} />
        <Route path="/eventos" element={<Eventos />} />
        <Route path="/asistentes" element={<Asistentes />} />
        <Route path="*" element={<h2>Página no encontrada</h2>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;