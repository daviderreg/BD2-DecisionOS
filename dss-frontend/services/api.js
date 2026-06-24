import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' }
});

export const DecisionAPI = {
  // CRUD
  getAll: () => api.get('/decisions'),
  getOne: (id) => api.get(`/decisions/${id}`),
  create: (data) => api.post('/decisions', data),
  update: (id, data) => api.put(`/decisions/${id}`, data),
  delete: (id) => api.delete(`/decisions/${id}`),
  
  // RAG
  ask: (question) => api.post('/ask', { question })
};