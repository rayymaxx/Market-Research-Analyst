import axios from 'axios';
import { ResearchRequest, ResearchResponse, KnowledgeStats, UploadResponse, ResearchHistoryItem } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
console.log('API_BASE_URL:', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token') || 'dev-token';
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const researchApi = {
  startResearch: async (request: ResearchRequest): Promise<ResearchResponse> => {
    console.log('Making request to:', `${API_BASE_URL}/research/start`);
    const response = await api.post('/research/start', request);
    return response.data;
  },

  getResearchStatus: async (researchId: string): Promise<ResearchResponse> => {
    const response = await api.get(`/research/${researchId}/status`);
    return response.data;
  },

  getResearchResult: async (researchId: string): Promise<any> => {
    const response = await api.get(`/research/${researchId}/result`);
    return response.data;
  },

  getResearchHistory: async (limit = 10, offset = 0): Promise<{ history: ResearchHistoryItem[], total: number }> => {
    const response = await api.get(`/research/history?limit=${limit}&offset=${offset}`);
    return response.data;
  },

  deleteResearch: async (researchId: string): Promise<void> => {
    await api.delete(`/research/${researchId}`);
  },
};

export const knowledgeApi = {
  getStats: async (): Promise<KnowledgeStats> => {
    const response = await api.get('/knowledge/stats');
    return response.data;
  },

  uploadFile: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/knowledge/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  listFiles: async (): Promise<any> => {
    const response = await api.get('/knowledge/files');
    return response.data;
  },

  deleteFile: async (filename: string): Promise<void> => {
    await api.delete(`/knowledge/files/${filename}`);
  },

  reindex: async (): Promise<void> => {
    await api.post('/knowledge/reindex');
  },
};

export const healthApi = {
  check: async (): Promise<any> => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;