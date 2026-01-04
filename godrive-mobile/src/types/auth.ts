export interface User {
  id: number; // ⚠️ Corrigido de string para number
  full_name: string | null;
  email: string;
  is_active: boolean;
  has_pending_reviews: boolean; // ✅ Novo campo adicionado
  user_type?: string; // ⚠️ Alerta: Backend atual NÃO está retornando isso
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface LoginCredentials {
  username: string; 
  password: string;
}