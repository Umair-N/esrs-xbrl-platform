// File: types/auth.ts
export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  is_active: boolean;
  is_verified: boolean;
  role: "user" | "admin";
  created_at: string;
}

export interface UserRegistration {
  email: string;
  username: string;
  password: string;
  full_name?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface RefreshTokenRequest {
  refresh_token: string;
}

export interface AuthResponse {
  message: string;
  user?: {
    id: number;
    email: string;
    username: string;
    full_name?: string;
  };
}

export interface ProtectedResponse {
  message: string;
}

export interface AuthContextType {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (credentials: LoginCredentials) => Promise<AuthTokens>;
  register: (userData: UserRegistration) => Promise<AuthResponse>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
}

export interface ApiError {
  detail: string;
  status_code?: number;
}

export interface AuthServiceTokens {
  accessToken: string | null;
  refreshToken: string | null;
}
