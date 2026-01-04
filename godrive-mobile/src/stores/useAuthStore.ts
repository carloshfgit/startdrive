// Arquivo: src/stores/useAuthStore.ts

import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { api } from '@/services/api';
import { LoginCredentials, RegisterData, TokenResponse, User } from '@/types/auth';

interface AuthState {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // Actions
  signIn: (credentials: LoginCredentials) => Promise<void>;
  signUp: (data: RegisterData) => Promise<void>; // ✅ Nova Action
  signOut: () => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      signIn: async ({ username, password }) => {
        set({ isLoading: true, error: null });
        try {
          // ⚠️ CORREÇÃO CRÍTICA PARA FASTAPI OAUTH2 ⚠️
          // O backend espera form-urlencoded, não JSON.
          const params = new URLSearchParams();
          params.append('username', username);
          params.append('password', password);

          const { data: tokenData } = await api.post<TokenResponse>(
            '/login/access-token', 
            params.toString(), // Envia como string formatada
            { 
               headers: { 'Content-Type': 'application/x-www-form-urlencoded' } 
            }
          );

          // Salva token temporariamente
          set({ token: tokenData.access_token });

          // Busca dados do usuário
          const { data: userData } = await api.get<User>('/users/me');

          set({
            token: tokenData.access_token,
            user: userData,
            isAuthenticated: true,
            isLoading: false,
          });

        } catch (error: any) {
            console.error(error);
            const msg = error.response?.data?.detail || 'Erro ao entrar. Verifique suas credenciais.';
            set({ 
                error: msg, 
                isLoading: false, 
                token: null, 
                isAuthenticated: false 
            });
            throw error; // Repassa erro para a tela tratar se precisar
        }
      },

      // ✅ Implementação do SignUp
      signUp: async (registerData) => {
        set({ isLoading: true, error: null });
        try {
          // 1. Cria o usuário (POST /users/)
          await api.post('/users/', registerData);
          
          // 2. Faz o login automático após cadastro (UX melhor)
          await get().signIn({ 
            username: registerData.email, 
            password: registerData.password 
          });
          
        } catch (error: any) {
          const msg = error.response?.data?.detail || 'Erro ao cadastrar. Tente outro email.';
          set({ isLoading: false, error: msg });
          throw error;
        }
      },

      signOut: () => {
        set({
          token: null,
          user: null,
          isAuthenticated: false,
          error: null,
        });
      },

      clearError: () => set({ error: null }),
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({ 
        token: state.token, 
        user: state.user, 
        isAuthenticated: state.isAuthenticated 
      }),
    }
  )
);