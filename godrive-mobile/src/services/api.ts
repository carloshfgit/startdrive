// Arquivo: src/services/api.ts

import axios from 'axios';
import { Platform } from 'react-native';
import { useAuthStore } from '@/stores/useAuthStore'; // Importação circular resolvida via getState()

// ⚠️ CONFIGURAÇÃO DE AMBIENTE
// Android Emulator: 10.0.2.2
// iOS Simulator: localhost
// Físico: Substitua pelo seu IP local (ex: http://192.168.x.x:8000/api/v1)
const LOCALHOST_ANDROID = 'http://10.0.2.2:8000/api/v1';
const LOCALHOST_IOS = 'http://localhost:8000/api/v1';

export const BASE_URL = Platform.OS === 'android' ? LOCALHOST_ANDROID : LOCALHOST_IOS;

export const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ----------------------------------------------------------------------
// 🕵️ INTERCEPTORS (O Segredo do Token)
// ----------------------------------------------------------------------

// Request: Injeta o Token JWT se existir
api.interceptors.request.use(
  async (config) => {
    // Acessa o token diretamente do estado do Zustand
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

// Response: Tratamento global de erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado ou inválido: força logout
      console.warn('⚠️ 401 Unauthorized - Deslogando usuário');
      useAuthStore.getState().signOut();
    }
    return Promise.reject(error);
  }
);