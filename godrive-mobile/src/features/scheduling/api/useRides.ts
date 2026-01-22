/**
 * useRides Hook
 * 
 * Hook React Query para gerenciar aulas (rides).
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/services/api';

interface Ride {
    id: number;
    student_id: number;
    instructor_id: number;
    scheduled_at: string;
    price: number;
    status: string;
    pickup_latitude?: number;
    pickup_longitude?: number;
}

interface CreateRideData {
    instructor_id: number;
    scheduled_at: string;
    pickup_latitude?: number;
    pickup_longitude?: number;
}

/**
 * Hook para buscar aulas do usuário.
 */
export function useRides() {
    return useQuery({
        queryKey: ['rides'],
        queryFn: async (): Promise<Ride[]> => {
            const { data } = await api.get<Ride[]>('/rides/');
            return data;
        },
    });
}

/**
 * Hook para criar um novo agendamento.
 */
export function useCreateRide() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: async (data: CreateRideData): Promise<Ride> => {
            const { data: ride } = await api.post<Ride>('/rides/', data);
            return ride;
        },
        onSuccess: () => {
            // Invalida cache para refetch
            queryClient.invalidateQueries({ queryKey: ['rides'] });
        },
    });
}
