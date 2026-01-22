/**
 * useSignUp Hook
 * 
 * Hook React Query para cadastro de novo usuário.
 * Usa useMutation para gerenciar o estado da mutation.
 */

import { useMutation } from '@tanstack/react-query';
import { api } from '@/services/api';
import { useSignIn } from './useSignIn';
import { RegisterData } from '@/types/auth';

/**
 * Hook para realizar cadastro com React Query mutation.
 * Após o cadastro bem sucedido, faz login automático.
 * 
 * @example
 * const { mutate: signUp, isPending } = useSignUp();
 * signUp({ email: 'user@email.com', password: '123456', full_name: 'User' });
 */
export function useSignUp() {
    const signInMutation = useSignIn();

    return useMutation({
        mutationFn: async (data: RegisterData): Promise<void> => {
            // 1. Criar o usuário
            await api.post('/users/', data);
        },
        onSuccess: async (_, variables) => {
            // 2. Fazer login automático após cadastro
            signInMutation.mutate({
                username: variables.email,
                password: variables.password,
            });
        },
    });
}
