// src/services/reportService.js
import api from './api';

/**
 * Obtiene estadísticas generales del dashboard.
 * GET /dashboard
 */
export function getDashboardStats() {
  return api.get('/dashboard')
    .then(res => res.data)
    .catch(err => Promise.reject(err));
}

/**
 * Reporte 1: Asistencia por evento.
 * GET /reportes/reportes/asistencia-eventos
 * @param {{ fecha_inicio?: string, fecha_fin?: string, evento_id?: number }} params
 */
export function getAsistenciaEventos(params = {}) {
  return api.get('/reportes/asistencia-eventos', { params })
    .then(res => res.data)
    .catch(err => Promise.reject(err));
}

/**
 * Reporte 2: Ventas totales por evento.
 * GET /reportes/reportes/ventas-totales
 * @param {{ fecha_inicio?: string, fecha_fin?: string, monto_minimo?: number, monto_maximo?: number }} params
 */
export function getVentasTotales(params = {}) {
  return api.get('/reportes/ventas-totales', { params })
    .then(res => res.data)
    .catch(err => Promise.reject(err));
}

/**
 * Reporte 3: Artistas populares.
 * GET /reportes/reportes/artistas-populares
 * @param {{ limite?: number, fecha_inicio?: string, fecha_fin?: string }} params
 */
export function getArtistasPopulares(params = {}) {
  return api.get('/reportes/artistas-populares', { params })
    .then(res => res.data)
    .catch(err => Promise.reject(err));
}

/**
 * Reporte 4: Eventos por categoría.
 * GET /reportes/reportes/eventos-por-categoria
 */
export function getEventosPorCategoria() {
  return api.get('/reportes/eventos-por-categoria')
    .then(res => res.data)
    .catch(err => Promise.reject(err));
}

/**
 * Reporte 5: Asistencia por ciudad.
 * GET /reportes/reportes/asistencia-por-ciudad
 */
export function getAsistenciaPorCiudad() {
  return api.get('/reportes/asistencia-por-ciudad')
    .then(res => res.data)
    .catch(err => Promise.reject(err));
}
