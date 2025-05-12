// src/components/Sidebar.jsx
import React from 'react';
import { NavLink } from 'react-router-dom';

export default function Sidebar() {
  const getActiveClass = ({ isActive }) =>
    isActive ? 'sidebar__link sidebar__link--active' : 'sidebar__link';

  return (
    <aside className="sidebar">
      <nav className="sidebar__nav">
        <NavLink to="/dashboard" className={getActiveClass}>
          Dashboard
        </NavLink>
        <NavLink to="/reporte1" className={getActiveClass}>
          Asistencia Eventos
        </NavLink>
        <NavLink to="/reporte2" className={getActiveClass}>
          Ventas Totales
        </NavLink>
        <NavLink to="/reporte3" className={getActiveClass}>
          Artistas Populares
        </NavLink>
        <NavLink to="/reporte4" className={getActiveClass}>
          Eventos por Categoría
        </NavLink>
        <NavLink to="/reporte5" className={getActiveClass}>
          Asistencia por Ciudad
        </NavLink>
      </nav>
    </aside>
  );
}
