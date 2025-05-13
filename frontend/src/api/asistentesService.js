// frontend/src/api/asistentesService.js
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const getAsistentes = async () => {
  const response = await axios.get(`${API_URL}/asistentes`);
  return response.data;
};

export const createAsistente = async (asistente) => {
  const response = await axios.post(`${API_URL}/asistentes`, asistente);
  return response.data;
};

export const updateAsistente = async (id, asistente) => {
  const response = await axios.put(`${API_URL}/asistentes/${id}`, asistente);
  return response.data;
};

export const deleteAsistente = async (id) => {
  await axios.delete(`${API_URL}/asistentes/${id}`);
};