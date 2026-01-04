import { api } from './api';
import { Instructor } from '@/types/instructor';

interface SearchParams {
  latitude: number;
  longitude: number;
  radius?: number; // Raio em KM (padrão 10km)
}

export const searchInstructors = async ({ latitude, longitude, radius = 10 }: SearchParams) => {
  try {
    // O backend espera query params na URL: ?lat=...&long=...&radius=...
    // Ajuste aqui se o seu backend usar nomes diferentes (ex: lat vs latitude)
    const response = await api.get<Instructor[]>('/instructors/search', {
      params: {
        latitude,
        longitude,
        radius_km: radius, // Verifique se o backend espera 'radius' ou 'radius_km'
      },
    });
    return response.data;
  } catch (error) {
    console.error('Erro ao buscar instrutores:', error);
    throw error;
  }
};