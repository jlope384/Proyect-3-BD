// frontend/src/pages/Asistentes.jsx
import { useState } from 'react';
import { getAsistentes, createAsistente, updateAsistente } from '../api/asistentesService';
import TablaMejorada from '../components/TablaMejorada';
import FormularioAsistente from '../components/FormularioAsistente';

const Asistentes = () => {
  const [asistentes, setAsistentes] = useState([]);
  const [mostrarFormulario, setMostrarFormulario] = useState(false);
  const [asistenteEditando, setAsistenteEditando] = useState(null);

  const cargarAsistentes = async () => {
    const data = await getAsistentes();
    setAsistentes(data);
  };

  const handleGuardar = async (asistente) => {
    if (asistenteEditando) {
      await updateAsistente(asistenteEditando.id, asistente);
    } else {
      await createAsistente(asistente);
    }
    cargarAsistentes();
    setMostrarFormulario(false);
  };

  const handleEditar = (id) => {
    const asistente = asistentes.find(a => a.id === id);
    setAsistenteEditando(asistente);
    setMostrarFormulario(true);
  };

  return (
    <div className="page-container">
      <h1>Gestión de Asistentes</h1>
      
      {mostrarFormulario ? (
        <FormularioAsistente
          asistenteExistente={asistenteEditando}
          onSave={handleGuardar}
          onCancel={() => setMostrarFormulario(false)}
        />
      ) : (
        <>
          <button onClick={() => {
            setAsistenteEditando(null);
            setMostrarFormulario(true);
          }}>
            Nuevo Asistente
          </button>
          <TablaMejorada
            datos={asistentes}
            columnas={['nombre', 'correo', 'fecha_nacimiento']}
            onEditar={handleEditar}
          />
        </>
      )}
    </div>
  );
};