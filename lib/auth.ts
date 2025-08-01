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

// const API_BASE_URL = "http://localhost:8000";
const API_BASE_URL = "https://esrs-xbrl-platform.onrender.com";

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

  // Helper method to parse response with better error handling
  private async parseResponse<T>(response: Response): Promise<T> {
    const contentType = response.headers.get("content-type");
    
    if (!contentType || !contentType.includes("application/json")) {
      const text = await response.text();
      console.error("Non-JSON response received:", {
        status: response.status,
        statusText: response.statusText,
        url: response.url,
        contentType,
        body: text.substring(0, 200) // Log first 200 chars
      });
      throw new Error(`Server returned ${response.status}: ${response.statusText}`);
    }

    try {
      return await response.json() as T;
    } catch (jsonError) {
      console.error("Failed to parse JSON response:", jsonError);
      throw new Error("Invalid JSON response from server");
    }
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

      const data = await this.parseResponse<AuthResponse | ApiError>(response);

      if (!response.ok) {
        const error = data as ApiError;
        throw new Error(error.detail || "Registration failed");
      }

      return data as AuthResponse;
    } catch (error) {
      console.error("Registration error:", error);
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

      const data = await this.parseResponse<AuthTokens | ApiError>(response);

      if (!response.ok) {
        const error = data as ApiError;
        throw new Error(error.detail || "Login failed");
      }

      const tokens = data as AuthTokens;

      // Save tokens
      this.setTokens(tokens.access_token, tokens.refresh_token);

      return tokens;
    } catch (error) {
      console.error("Login error:", error);
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

      const data = await this.parseResponse<{ access_token: string } | ApiError>(response);

      if (!response.ok) {
        const error = data as ApiError;
        throw new Error(error.detail || "Token refresh failed");
      }

      // Update access token
      const { refreshToken: currentRefreshToken } = this.getTokens();
      if (currentRefreshToken) {
        const tokenData = data as { access_token: string };
        this.setTokens(tokenData.access_token, currentRefreshToken);
        return tokenData.access_token;
      }

      throw new Error("Failed to update tokens");
    } catch (error) {
      console.error("Token refresh error:", error);
      // If refresh fails, remove tokens
      this.removeTokens();
      throw error;
    }
  }

  // Make authenticated API request with improved error handling
  async makeAuthenticatedRequest(
    url: string,
    options: RequestInit = {}
  ): Promise<Response> {
    const { accessToken } = this.getTokens();

    if (!accessToken) {
      throw new Error("No access token available");
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          ...options.headers,
          Authorization: `Bearer ${accessToken}`,
        },
      });

      // If token is expired, try to refresh
      if (response.status === 401) {
        console.log("Access token expired, attempting to refresh...");
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
          console.error("Token refresh failed:", refreshError);
          throw new Error("Authentication failed - please login again");
        }
      }

      return response;
    } catch (error) {
      console.error("Authenticated request failed:", {
        url,
        error: error instanceof Error ? error.message : error
      });
      throw error;
    }
  }

  // Get current user info
  async getCurrentUser(): Promise<User> {
    try {
      console.log("Fetching current user from:", `${this.baseURL}/me`);
      
      const response = await this.makeAuthenticatedRequest(
        `${this.baseURL}/me`
      );

      if (!response.ok) {
        console.error("getCurrentUser failed:", {
          status: response.status,
          statusText: response.statusText,
          url: response.url
        });
        throw new Error(`Failed to get user info: ${response.status} ${response.statusText}`);
      }

      const user = await this.parseResponse<User>(response);
      console.log("User fetched successfully:", { id: user.id, username: user.username });
      return user;
    } catch (error) {
      console.error("getCurrentUser error:", error);
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
        throw new Error(`Failed to access protected route: ${response.status} ${response.statusText}`);
      }

      return await this.parseResponse<ProtectedResponse>(response);
    } catch (error) {
      console.error("getProtectedData error:", error);
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
        throw new Error(`Failed to access admin route: ${response.status} ${response.statusText}`);
      }

      return await this.parseResponse<ProtectedResponse>(response);
    } catch (error) {
      console.error("getAdminData error:", error);
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
        throw new Error(`Failed to get users: ${response.status} ${response.statusText}`);
      }

      return await this.parseResponse<User[]>(response);
    } catch (error) {
      console.error("getAllUsers error:", error);
      throw error;
    }
  }

  // Health check method to test API connectivity
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseURL}/health`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
      
      return response.ok;
    } catch (error) {
      console.error("Health check failed:", error);
      return false;
    }
  }
}

export default new AuthService();