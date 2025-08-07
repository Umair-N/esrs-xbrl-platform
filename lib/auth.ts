// File: lib/auth.ts (Merged AuthService)
import axiosInstance from './axios';
import { 
  LoginCredentials, 
  UserRegistration, 
  User, 
  AuthTokens, 
  AuthResponse
} from '../types/auth';

class AuthService {
  private accessTokenKey = 'access_token'; // Using old version's key for compatibility
  private refreshTokenKey = 'refreshToken';
  private accessToken: string | null = null;

  constructor() {
    // Load token from storage on initialization (from old version)
    if (typeof window !== "undefined") {
      const storedToken = localStorage.getItem(this.accessTokenKey);
      if (storedToken) {
        this.accessToken = storedToken;
      }
    }
  }

  // Synchronous token check for React Query enabled condition (from new version)
  hasValidToken(): boolean {
    if (typeof window === 'undefined') return false;
    const token = localStorage.getItem(this.accessTokenKey);
    return !!token;
  }

  // Keep the async version for compatibility (merged approach)
  async isAuthenticated(): Promise<boolean> {
    if (typeof window === 'undefined') return false;
    
    const token = this.getAccessToken();
    if (!token) return false;

    try {
      // Verify token with server
      await this.getCurrentUser();
      return true;
    } catch (error) {
      // Token might be invalid - clear it
      this.clearTokens();
      return false;
    }
  }

  getAccessToken(): string | null {
    if (typeof window === 'undefined') return null;
    // Return in-memory token first, fallback to localStorage
    return this.accessToken || localStorage.getItem(this.accessTokenKey);
  }

  getRefreshToken(): string | null {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem(this.refreshTokenKey);
  }

  // New version's method for setting both tokens
  setTokens(tokens: AuthTokens): void {
    if (typeof window === 'undefined') return;
    
    this.accessToken = tokens.accessToken;
    localStorage.setItem(this.accessTokenKey, tokens.accessToken);
    
    if (tokens.refreshToken) {
      localStorage.setItem(this.refreshTokenKey, tokens.refreshToken);
    }
  }

  // Old version's method for backward compatibility
  setAccessToken(token: string): void {
    this.accessToken = token;
    if (typeof window !== "undefined") {
      localStorage.setItem(this.accessTokenKey, token);
    }
  }

  // New version's method
  clearTokens(): void {
    if (typeof window === 'undefined') return;
    this.accessToken = null;
    localStorage.removeItem(this.accessTokenKey);
    localStorage.removeItem(this.refreshTokenKey);
  }

  // Old version's method for backward compatibility
  clearAccessToken(): void {
    this.clearTokens(); // Delegate to the more comprehensive method
  }

  async login(credentials: LoginCredentials): Promise<AuthTokens> {
    try {
      // Try new version's endpoint first, fallback to old version's
      let response;

try {
  response = await axiosInstance.post('/api/v1/auth/login', credentials);
} catch (error: any) {
  if (error.response?.status === 404) {
    // Optional: Handle 404 if even this fallback fails
    console.error("Login endpoint not found.");
  }
  throw error;
}


      // Handle both response formats
      const tokens: AuthTokens = {
        accessToken: response.data.accessToken || response.data.access_token,
        refreshToken: response.data.refreshToken,
      };
      
      this.setTokens(tokens);
      return { ...tokens, user: response.data.user };
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Login failed');
    }
  }

  async register(userData: UserRegistration): Promise<AuthResponse> {
    try {
      // Try new version's endpoint first, fallback to old version's
      let response;
      try {
        response = await axiosInstance.post('/auth/register', userData);
      } catch (error: any) {
        if (error.response?.status === 404) {
          // Fallback to old version's endpoint
          response = await axiosInstance.post('/api/v1/auth/register', userData);
        } else {
          throw error;
        }
      }
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Registration failed');
    }
  }

  async getCurrentUser(): Promise<User> {
    try {
      // Try new version's endpoint first, fallback to old version's
      let response;
      try {
        response = await axiosInstance.get('/auth/me');
      } catch (error: any) {
        if (error.response?.status === 404) {
          // Fallback to old version's endpoint
          response = await axiosInstance.get('/api/v1/users/me');
        } else {
          throw error;
        }
      }
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || 'Failed to get user data');
    }
  }

  async refreshToken(): Promise<string> {
    try {
      const refreshToken = this.getRefreshToken();
      
      let response;
      if (refreshToken) {
        // New version approach with refresh token
        response = await axiosInstance.post('/auth/refresh', {
          refreshToken,
        });
      } else {
        // Old version approach (might use cookies or session)
        try {
          response = await axiosInstance.post('/auth/refresh');
        } catch (error: any) {
          if (error.response?.status === 404) {
            response = await axiosInstance.post('/api/v1/auth/refresh');
          } else {
            throw error;
          }
        }
      }

      const newTokens: AuthTokens = {
        accessToken: response.data.accessToken || response.data.access_token,
        refreshToken: response.data.refreshToken || refreshToken,
      };

      this.setTokens(newTokens);
      return newTokens.accessToken;
    } catch (error: any) {
      this.clearTokens();
      throw new Error(error.response?.data?.message || 'Token refresh failed');
    }
  }

  async logout(): Promise<void> {
    try {
      // Try new version's endpoint first, fallback to old version's
      try {
        await axiosInstance.post('/auth/logout');
      } catch (error: any) {
        if (error.response?.status === 404) {
          await axiosInstance.post('/api/v1/auth/logout');
        } else {
          throw error;
        }
      }
    } catch (error) {
      // Continue with logout even if server call fails
      console.error('Logout API call failed:', error);
    } finally {
      this.clearTokens();
    }
  }

  // Additional methods from old version for backward compatibility
  async getProtectedData(): Promise<any> {
    const response = await axiosInstance.get("/protected");
    return response.data;
  }

  async getAdminData(): Promise<any> {
    const response = await axiosInstance.get("/admin-only");
    return response.data;
  }

  async getAllUsers(): Promise<User[]> {
    const response = await axiosInstance.get("/users");
    return response.data as User[];
  }
}

export default new AuthService();