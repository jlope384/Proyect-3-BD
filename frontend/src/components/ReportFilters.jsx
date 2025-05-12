// src/components/ReportFilters.jsx
import React, { useState } from 'react';

/**
 * fields: [
 *   { name: 'fecha_inicio', label: 'Fecha Inicio', type: 'date' },
 *   { name: 'fecha_fin',    label: 'Fecha Fin',    type: 'date' },
 *   { name: 'evento_id',    label: 'ID Evento',    type: 'number' },
 *   ...
 * ]
 */
export default function ReportFilters({ fields, onSubmit }) {
  const initial = fields.reduce((acc, f) => ({ ...acc, [f.name]: '' }), {});
  const [values, setValues] = useState(initial);

  const handleChange = e => {
    const { name, value } = e.target;
    setValues(v => ({ ...v, [name]: value }));
  };

  const handleSubmit = e => {
    e.preventDefault();
    // Limpia strings vacíos para no enviarlos
    const params = Object.entries(values).reduce((acc, [k, v]) => {
      if (v !== '') acc[k] = v;
      return acc;
    }, {});
    onSubmit(params);
  };

  return (
    <form className="report-filters" onSubmit={handleSubmit}>
      {fields.map(f => (
        <div className="filter-field" key={f.name}>
          <label htmlFor={f.name}>{f.label}</label>
          <input
            id={f.name}
            name={f.name}
            type={f.type || 'text'}
            value={values[f.name]}
            onChange={handleChange}
          />
        </div>
      ))}
      <button type="submit">Aplicar filtros</button>
    </form>
  );
}
