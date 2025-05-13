// frontend/src/components/FormularioAsistente.jsx
import { useState } from 'react';

const FormularioAsistente = ({ asistenteExistente, onSave, onCancel }) => {
  const [asistente, setAsistente] = useState(asistenteExistente || {
    nombre: '',
    correo: '',
    fecha_nacimiento: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(asistente);
  };

  return (
    <form onSubmit={handleSubmit} className="form-container">
      <div className="form-group">
        <label>Nombre:</label>
        <input
          type="text"
          value={asistente.nombre}
          onChange={(e) => setAsistente({...asistente, nombre: e.target.value})}
          required
        />
      </div>
      
      <div className="form-group">
        <label>Correo:</label>
        <input
          type="email"
          value={asistente.correo}
          onChange={(e) => setAsistente({...asistente, correo: e.target.value})}
          required
        />
      </div>

      <div className="form-group">
        <label>Fecha Nacimiento:</label>
        <input
          type="date"
          value={asistente.fecha_nacimiento}
          onChange={(e) => setAsistente({...asistente, fecha_nacimiento: e.target.value})}
          required
        />
      </div>

      <div className="form-actions">
        <button type="submit">Guardar</button>
        <button type="button" onClick={onCancel}>Cancelar</button>
      </div>
    </form>
  );
};
