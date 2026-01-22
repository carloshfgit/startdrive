/**
 * QueryClient Configuration
 * 
 * Configuração centralizada do TanStack Query (React Query).
 * Gerencia cache, retry, stale time para todas as queries do app.
 */

import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            // Tempo que os dados são considerados "frescos" (não refetch automático)
            staleTime: 1000 * 60 * 5, // 5 minutos

            // Tempo que os dados ficam em cache após não serem mais usados
            gcTime: 1000 * 60 * 30, // 30 minutos (antigo cacheTime)

            // Número de tentativas em caso de erro
            retry: 2,

            // Não refetch ao voltar para a janela (melhor para mobile)
            refetchOnWindowFocus: false,

            // Não refetch ao reconectar (evita uso excessivo de dados móveis)
            refetchOnReconnect: false,
        },
        mutations: {
            // Apenas 1 retry para mutations
            retry: 1,
        },
    },
});
