// File: types/auth.ts (Updated types)
export interface User {
  id: string;
  email: string;
  name?: string;
  role?: string;
  // Add other user properties as needed
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface UserRegistration {
  email: string;
  password: string;
  name?: string;
  // Add other registration fields as needed
}

export interface AuthTokens {
  accessToken: string;
  refreshToken?: string;
  user?: User; // Optional user data returned from login
}

export interface AuthResponse {
  user: User;
  message?: string;
}

// Updated AuthContextType for React Query integration
export interface AuthContextType {
  // User data and auth state
  user: User | null | undefined;
  loading: boolean;
  isAuthenticated: boolean;
  
  login: (credentials: LoginCredentials) => Promise<AuthTokens>;
  register: (userData: UserRegistration) => Promise<AuthResponse>;
  logout: () => Promise<void>;
  
  // Utility
  // refetchUser: () => void;
}