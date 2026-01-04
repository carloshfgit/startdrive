// Arquivo: src/stores/useAuthStore.ts

import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { api } from '@/services/api';
import { LoginCredentials, TokenResponse, User } from '@/types/auth';

interface AuthState {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // Actions
  signIn: (credentials: LoginCredentials) => Promise<void>;
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
          // 1. Obter o Token (OAuth2 standard form-data vs JSON)
          // O dev-mobile indica JSON. Se der erro 422, troque para form-urlencoded.
          const { data: tokenData } = await api.post<TokenResponse>(
            '/login/access-token', 
            { username, password },
            { 
               headers: { 'Content-Type': 'application/x-www-form-urlencoded' } // FastAPI OAuth2 padrão exige isso
            }
          );

          // Salva o token temporariamente para a próxima requisição usar
          set({ token: tokenData.access_token });

          // 2. Com o token salvo, buscamos os dados do usuário logado
          const { data: userData } = await api.get<User>('/users/me');

          set({
            token: tokenData.access_token,
            user: userData,
            isAuthenticated: true,
            isLoading: false,
          });

        } catch (error: any) {
            const msg = error.response?.data?.detail || 'Erro ao entrar. Verifique seus dados.';
            set({ 
                error: msg, 
                isLoading: false, 
                token: null, 
                isAuthenticated: false 
            });
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