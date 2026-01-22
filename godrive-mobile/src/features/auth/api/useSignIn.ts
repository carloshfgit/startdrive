/**
 * useSignIn Hook
 * 
 * Hook React Query para autenticação (login).
 * Usa useMutation para gerenciar o estado da mutation.
 */

import { useMutation } from '@tanstack/react-query';
import { api } from '@/services/api';
import { useAuthStore } from '@/stores/useAuthStore';
import { TokenResponse, User } from '@/types/auth';

interface SignInData {
    username: string;
    password: string;
}

/**
 * Hook para realizar login com React Query mutation.
 * 
 * @example
 * const { mutate: signIn, isPending, isError } = useSignIn();
 * signIn({ username: 'user@email.com', password: '123456' });
 */
export function useSignIn() {
    const setToken = useAuthStore((state) => state.token ? () => { } : () => { });

    return useMutation({
        mutationFn: async (data: SignInData): Promise<{ token: TokenResponse; user: User }> => {
            // 1. Fazer login e obter token
            const params = new URLSearchParams();
            params.append('username', data.username);
            params.append('password', data.password);

            const tokenResponse = await api.post<TokenResponse>(
                '/login/access-token',
                params.toString(),
                { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
            );

            // 2. Configurar token temporariamente para buscar usuário
            api.defaults.headers.common['Authorization'] = `Bearer ${tokenResponse.data.access_token}`;

            // 3. Buscar dados do usuário
            const userResponse = await api.get<User>('/users/me');

            return {
                token: tokenResponse.data,
                user: userResponse.data,
            };
        },
        onSuccess: (data) => {
            // Atualiza o store com token e usuário
            useAuthStore.getState().setAuth(data.token.access_token, data.user);
        },
        onError: () => {
            // Limpa o header em caso de erro
            delete api.defaults.headers.common['Authorization'];
        },
    });
}
