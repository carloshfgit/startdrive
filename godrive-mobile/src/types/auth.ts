// Arquivo: src/types/auth.ts

// O que recebemos do backend (UserResponse)
export interface User {
  id: number;
  full_name: string | null;
  email: string;
  is_active: boolean;
  has_pending_reviews: boolean;
  user_type: 'student' | 'instructor' | null; // ✅ Atualizado conforme schema
}

// O que recebemos ao logar
export interface TokenResponse {
  access_token: string;
  token_type: string;
}

// Dados para Login
export interface LoginCredentials {
  username: string; // Email
  password: string;
}

// ✅ Novo: Dados para Cadastro (UserCreate)
export interface RegisterData {
  full_name: string;
  email: string;
  password: string;
  user_type: 'student' | 'instructor' | null;
}