// frontend/src/api/reportesService.js
import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const getReporteAsistencia = async (filtros) => {
  try {
    const response = await axios.post(`${API_URL}/reporte-asistencia`, filtros);
    return response.data;
  } catch (error) {
    console.error('Error al obtener reporte:', error);
    return [];
  }
};