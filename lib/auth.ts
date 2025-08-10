// File: lib/auth.ts
import axiosInstance from "./axios";
import {
  LoginCredentials,
  UserRegistration,
  User,
  AuthTokens,
  AuthResponse,
} from "../types/auth";

class AuthService {
  private accessTokenKey = "access_token";
  private refreshTokenKey = "refresh_token";
  private accessToken: string | null = null;

  constructor() {
    if (typeof window !== "undefined") {
      const storedToken = localStorage.getItem(this.accessTokenKey);
      if (storedToken) {
        this.accessToken = storedToken;
      }
    }

    // Bind methods to preserve 'this' context
    this.login = this.login.bind(this);
    this.register = this.register.bind(this);
    this.logout = this.logout.bind(this);
    this.getCurrentUser = this.getCurrentUser.bind(this);
    this.refreshToken = this.refreshToken.bind(this);
    this.setTokens = this.setTokens.bind(this);
    this.clearTokens = this.clearTokens.bind(this);
    this.getAccessToken = this.getAccessToken.bind(this);
    this.isAuthenticated = this.isAuthenticated.bind(this);
    this.hasValidToken = this.hasValidToken.bind(this);
  }

  hasValidToken(): boolean {
    if (typeof window === "undefined") return false;
    const token = localStorage.getItem(this.accessTokenKey);
    return !!token;
  }

  async isAuthenticated(): Promise<boolean> {
    if (typeof window === "undefined") return false;

    const token = this.getAccessToken();
    if (!token) return false;

    try {
      await this.getCurrentUser();
      return true;
    } catch (error) {
      this.clearTokens();
      return false;
    }
  }

  getAccessToken(): string | null {
    if (typeof window === "undefined") return null;
    return this.accessToken || localStorage.getItem(this.accessTokenKey);
  }

  setTokens(tokens: AuthTokens): void {
    if (typeof window === "undefined") {
      console.log("[AuthService] setTokens skipped: window undefined");
      return;
    }

    this.accessToken = tokens.accessToken;
    localStorage.setItem(this.accessTokenKey, tokens.accessToken);

    if (tokens.refreshToken) {
      localStorage.setItem(this.refreshTokenKey, tokens.refreshToken);
      console.log(
        "[AuthService] setTokens: refreshToken stored",
        tokens.refreshToken
      );
    }
  }

  clearTokens(): void {
    if (typeof window === "undefined") return;
    this.accessToken = null;
    localStorage.removeItem(this.accessTokenKey);
    localStorage.removeItem(this.refreshTokenKey);
  }

  async login(credentials: LoginCredentials): Promise<AuthTokens> {
    try {
      const response = await axiosInstance.post("/auth/login", credentials);

      // Adjust if your backend uses snake_case or camelCase here:
      const tokens: AuthTokens = {
        accessToken: response.data.accessToken || response.data.access_token,
        refreshToken: response.data.refreshToken || response.data.refresh_token,
      };

      this.setTokens(tokens);

      return { ...tokens };
    } catch (error: any) {
      console.error("[AuthService] login error", error);
      throw new Error(error.response?.data?.message || "Login failed");
    }
  }

  async register(userData: UserRegistration): Promise<AuthResponse> {
    try {
      const response = await axiosInstance.post("/auth/register", userData);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.message || "Registration failed");
    }
  }

  async getCurrentUser(): Promise<User> {
    try {
      const response = await axiosInstance.get("/users/me");
      return response.data;
    } catch (error: any) {
      throw new Error(
        error.response?.data?.message || "Failed to get user data"
      );
    }
  }

  async refreshToken(): Promise<string> {
    try {
      const response = await axiosInstance.post("/auth/refresh", null, {
        withCredentials: true,
      });

      const newAccessToken =
        response.data.accessToken || response.data.access_token;

      this.setTokens({
        accessToken: newAccessToken,
      });

      return newAccessToken;
    } catch (error: any) {
      this.clearTokens();
      throw new Error(error.response?.data?.message || "Token refresh failed");
    }
  }

  async ensureAccessToken(): Promise<string | null> {
    if (!this.hasValidToken()) {
      try {
        const newToken = await this.refreshToken();
        return newToken;
      } catch {
        this.clearTokens();
        return null;
      }
    }
    return this.getAccessToken();
  }

  async logout(): Promise<void> {
    try {
      await axiosInstance.post("/auth/logout");
    } catch (error) {
      console.error("Logout API call failed:", error);
    } finally {
      this.clearTokens();
    }
  }
}

export default new AuthService();
