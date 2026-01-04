// Arquivo: src/services/api.ts

import axios from 'axios';
import { useAuthStore } from '@/stores/useAuthStore'; 
import { ENV } from '@/config/env'; // <--- Importação da config

export const api = axios.create({
  baseURL: ENV.API_URL, // Usa a URL definida no env.ts
  timeout: ENV.TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ... (Mantenha os interceptors de Request e Response exatamente como estavam) ...
api.interceptors.request.use(
  async (config) => {
    const token = useAuthStore.getState().token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().signOut();
    }
    return Promise.reject(error);
  }
);