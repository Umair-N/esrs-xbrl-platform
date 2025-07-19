// File: lib/auth.ts
import {
  User,
  UserRegistration,
  LoginCredentials,
  AuthTokens,
  RefreshTokenRequest,
  AuthResponse,
  ProtectedResponse,
  AuthServiceTokens,
  ApiError,
} from "../types/auth";

const API_BASE_URL = "http://localhost:8000";
// const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL!;

class AuthService {
  private baseURL: string;

  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Get tokens from localStorage
  getTokens(): AuthServiceTokens {
    if (typeof window === "undefined") {
      return { accessToken: null, refreshToken: null };
    }

    const accessToken = localStorage.getItem("access_token");
    const refreshToken = localStorage.getItem("refresh_token");

    return { accessToken, refreshToken };
  }

  // Save tokens to localStorage
  setTokens(accessToken: string, refreshToken: string): void {
    if (typeof window === "undefined") return;

    localStorage.setItem("access_token", accessToken);
    localStorage.setItem("refresh_token", refreshToken);
  }

  // Remove tokens from localStorage
  removeTokens(): void {
    if (typeof window === "undefined") return;

    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  }

  // Check if user is authenticated
  isAuthenticated(): boolean {
    const { accessToken } = this.getTokens();
    return !!accessToken;
  }

  // Register new user
  async register(userData: UserRegistration): Promise<AuthResponse> {
    try {
      const response = await fetch(`${this.baseURL}/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();

      if (!response.ok) {
        const error = data as ApiError;
        throw new Error(error.detail || "Registration failed");
      }

      return data as AuthResponse;
    } catch (error) {
      throw error;
    }
  }

  // Login user
  async login(credentials: LoginCredentials): Promise<AuthTokens> {
    try {
      const response = await fetch(`${this.baseURL}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(credentials),
      });

      const data = await response.json();

      if (!response.ok) {
        const error = data as ApiError;
        throw new Error(error.detail || "Login failed");
      }

      const tokens = data as AuthTokens;

      // Save tokens
      this.setTokens(tokens.access_token, tokens.refresh_token);

      return tokens;
    } catch (error) {
      throw error;
    }
  }

  // Logout user
  async logout(): Promise<void> {
    try {
      const { refreshToken } = this.getTokens();

      if (refreshToken) {
        const logoutData: RefreshTokenRequest = { refresh_token: refreshToken };

        await fetch(`${this.baseURL}/logout`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(logoutData),
        });
      }
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      this.removeTokens();
    }
  }

  // Refresh access token
  async refreshToken(): Promise<string> {
    try {
      const { refreshToken } = this.getTokens();

      if (!refreshToken) {
        throw new Error("No refresh token available");
      }

      const refreshData: RefreshTokenRequest = { refresh_token: refreshToken };

      const response = await fetch(`${this.baseURL}/refresh`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(refreshData),
      });

      const data = await response.json();

      if (!response.ok) {
        const error = data as ApiError;
        throw new Error(error.detail || "Token refresh failed");
      }

      // Update access token
      const { refreshToken: currentRefreshToken } = this.getTokens();
      if (currentRefreshToken) {
        this.setTokens(data.access_token, currentRefreshToken);
      }

      return data.access_token;
    } catch (error) {
      // If refresh fails, remove tokens
      this.removeTokens();
      throw error;
    }
  }

  // Make authenticated API request
  async makeAuthenticatedRequest(
    url: string,
    options: RequestInit = {}
  ): Promise<Response> {
    const { accessToken } = this.getTokens();

    if (!accessToken) {
      throw new Error("No access token available");
    }

    const response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        Authorization: `Bearer ${accessToken}`,
      },
    });

    // If token is expired, try to refresh
    if (response.status === 401) {
      try {
        const newAccessToken = await this.refreshToken();

        // Retry the original request with new token
        return await fetch(url, {
          ...options,
          headers: {
            ...options.headers,
            Authorization: `Bearer ${newAccessToken}`,
          },
        });
      } catch (refreshError) {
        throw new Error("Authentication failed");
      }
    }

    return response;
  }

  // Get current user info
  async getCurrentUser(): Promise<User> {
    try {
      const response = await this.makeAuthenticatedRequest(
        `${this.baseURL}/me`
      );

      if (!response.ok) {
        throw new Error("Failed to get user info");
      }

      return (await response.json()) as User;
    } catch (error) {
      throw error;
    }
  }

  // Access protected route
  async getProtectedData(): Promise<ProtectedResponse> {
    try {
      const response = await this.makeAuthenticatedRequest(
        `${this.baseURL}/protected`
      );

      if (!response.ok) {
        throw new Error("Failed to access protected route");
      }

      return (await response.json()) as ProtectedResponse;
    } catch (error) {
      throw error;
    }
  }

  // Access admin-only route
  async getAdminData(): Promise<ProtectedResponse> {
    try {
      const response = await this.makeAuthenticatedRequest(
        `${this.baseURL}/admin-only`
      );

      if (!response.ok) {
        throw new Error("Failed to access admin route");
      }

      return (await response.json()) as ProtectedResponse;
    } catch (error) {
      throw error;
    }
  }

  // Get all users (admin only)
  async getAllUsers(): Promise<User[]> {
    try {
      const response = await this.makeAuthenticatedRequest(
        `${this.baseURL}/users`
      );

      if (!response.ok) {
        throw new Error("Failed to get users");
      }

      return (await response.json()) as User[];
    } catch (error) {
      throw error;
    }
  }
}

export default new AuthService();
