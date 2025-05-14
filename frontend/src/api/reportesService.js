import axios from 'axios';

const API_URL = 'http://localhost:8000/api/reportes';

export const getAsistenciaEvento = (filtros) => {
  return axios.get(`${API_URL}/asistencia-evento`, { params: filtros });
};

export const getVentasTotales = (filtros) => {
  return axios.get(`${API_URL}/ventas-totales`, { params: filtros });
};

export const getArtistasPopulares = (filtros) => {
  return axios.get(`${API_URL}/artistas-populares`, { params: filtros });
};

export const getEventosPorCategoria = (filtros) => {
  return axios.get(`${API_URL}/eventos-por-categoria`, { params: filtros });
};

export const getAsistenciaPorCiudad = (filtros) => {
  return axios.get(`${API_URL}/asistencia-por-ciudad`, { params: filtros });
};

export const getTiposArtista = () => {
  return axios.get(`${API_URL}/tipos-artista`);
};

export const getCiudades = () => axios.get('http://localhost:8000/api/ciudades');
export const getCategorias = () => axios.get('http://localhost:8000/api/categoria-evento');
export const getTiposEntrada = () => axios.get('http://localhost:8000/api/tipo-entrada');
export const getMediosPago = () => axios.get('http://localhost:8000/api/medio-pago');