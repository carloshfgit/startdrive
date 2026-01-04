export interface Instructor {
  id: number;
  user_id: number;
  full_name: string; // Vem do join com User
  avatar_url?: string; // Opcional
  rating: number; // Ex: 4.8
  car_model: string; // Ex: "HB20 2022"
  hourly_rate: number; // Ex: 60.00
  latitude: number;
  longitude: number;
  distance?: number; // Backend calcula a distância
}