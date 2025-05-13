import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const getEventos = async () => {
  try {
    const response = await axios.get(`${API_URL}/eventos`);
    return response.data;
  } catch (error) {
    console.error('Error al obtener eventos:', error);
    return [];
  }
};