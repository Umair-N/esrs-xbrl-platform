import axiosInstance from "./axios";
import {
  User,
  UserRegistration,
  LoginCredentials,
  AuthResponse,
  ProtectedResponse,
  AuthTokens,
} from "../types/auth";

let accessToken: string | null = null;

class AuthService {
  constructor() {
    // Load token from storage on initialization
    if (typeof window !== "undefined") {
      const storedToken = localStorage.getItem("access_token");
      if (storedToken) {
        accessToken = storedToken;
      }
    }
  }

  getAccessToken(): string | null {
    return accessToken;
  }

  setAccessToken(token: string): void {
    accessToken = token;
    // Persist token
    if (typeof window !== "undefined") {
      localStorage.setItem("access_token", token);
    }
  }

  clearAccessToken(): void {
    accessToken = null;
    if (typeof window !== "undefined") {
      localStorage.removeItem("access_token");
    }
  }

  async isAuthenticated(): Promise<boolean> {
    try {
      await this.getCurrentUser();
      return true;
    } catch (error) {
      // Clear invalid token
      this.clearAccessToken();
      return false;
    }
  }

  async register(userData: UserRegistration): Promise<AuthResponse> {
    const response = await axiosInstance.post(
      "/api/v1/auth/register",
      userData
    );
    return response.data;
  }

  async login(credentials: LoginCredentials): Promise<AuthTokens> {
    const response = await axiosInstance.post(
      "/api/v1/auth/login",
      credentials
    );

    const tokens = response.data;
    this.setAccessToken(tokens.access_token);
    return tokens;
  }

  async logout(): Promise<void> {
    try {
      await axiosInstance.post("/api/v1/auth/logout");
    } catch (error) {
      console.warn("Logout request failed:", error);
    } finally {
      this.clearAccessToken();
    }
  }

  async refreshToken(): Promise<string> {
    const response = await axiosInstance.post("/api/v1/auth/refresh");
    const newAccessToken = response.data.access_token;
    this.setAccessToken(newAccessToken);
    return newAccessToken;
  }

  async getCurrentUser(): Promise<User> {
    const response = await axiosInstance.get("/api/v1/users/me");
    return response.data as User;
  }

  async getProtectedData(): Promise<ProtectedResponse> {
    const response = await axiosInstance.get("/protected");
    return response.data as ProtectedResponse;
  }

  async getAdminData(): Promise<ProtectedResponse> {
    const response = await axiosInstance.get("/admin-only");
    return response.data as ProtectedResponse;
  }

  async getAllUsers(): Promise<User[]> {
    const response = await axiosInstance.get("/users");
    return response.data as User[];
  }
}

const authService = new AuthService();
export default authService;
