/**
 * useInstructors Hook
 * 
 * Hook React Query para buscar instrutores por geolocalização.
 * Usa useQuery para cache automático e refetch.
 */

import { useQuery } from '@tanstack/react-query';
import { api } from '@/services/api';

interface SearchParams {
    latitude: number;
    longitude: number;
    radius?: number;
}

interface Instructor {
    id: number;
    full_name: string;
    bio?: string;
    hourly_rate: number;
    cnh_category?: string;
    vehicle_model?: string;
    distance?: number;
}

/**
 * Hook para buscar instrutores próximos usando React Query.
 * 
 * @param params - Parâmetros de busca (lat, lng, radius)
 * @returns Query result com lista de instrutores
 * 
 * @example
 * const { data: instructors, isLoading } = useInstructors({
 *   latitude: -23.55,
 *   longitude: -46.63,
 *   radius: 10
 * });
 */
export function useInstructors(params: SearchParams) {
    return useQuery({
        // Chave única para cache baseada nos parâmetros
        queryKey: ['instructors', params.latitude, params.longitude, params.radius ?? 10],

        queryFn: async (): Promise<Instructor[]> => {
            const { data } = await api.get<Instructor[]>('/instructors/search', {
                params: {
                    latitude: params.latitude,
                    longitude: params.longitude,
                    radius: params.radius ?? 10,
                },
            });
            return data;
        },

        // Só executa se tiver coordenadas válidas
        enabled: !!params.latitude && !!params.longitude,

        // Cache por 1 minuto (dados de localização podem mudar)
        staleTime: 1000 * 60,

        // Placeholder enquanto carrega
        placeholderData: [],
    });
}
