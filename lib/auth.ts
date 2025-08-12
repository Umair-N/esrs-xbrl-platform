import {
  queryOptions,
  useMutation,
  useQuery,
  useQueryClient,
} from '@tanstack/react-query';
import { z } from 'zod';

import { AuthResponse, User } from '@/types/api';

import { api } from './api-client';

export const getUser = async (): Promise<User> => {
  const response = (await api.get('/users/me')) as User;

  return response;
};

const userQueryKey = ['user'];

export const getUserQueryOptions = () => {
  return queryOptions({
    queryKey: userQueryKey,
    queryFn: getUser,
    refetchOnMount: false,
    retry: false,
  });
};

export const useUser = () => useQuery(getUserQueryOptions());

export const useLogin = ({ onSuccess, onError }: { onSuccess?: () => void, onError?: (err: Error) => void }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: loginWithEmailAndPassword,
    onSuccess: (data) => {
      queryClient.setQueryData(userQueryKey, data.user);
      onSuccess?.();
    },
    onError: (err) => {
      onError?.(err);
    },
  });
};

export const useRegister = ({ onSuccess, onError }: { onSuccess?: () => void, onError?: (err: Error) => void }) => {
  // const queryClient = useQueryClient();
  return useMutation({
    mutationFn: registerUser,
    onSuccess: (data) => {
      // queryClient.setQueryData(userQueryKey, data.user);
      onSuccess?.();
    },
    onError: (err) => {
      onError?.(err);
    },
  });
};

export const useLogout = ({ onSuccess }: { onSuccess?: () => void }) => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: logout,
    onSuccess: () => {
      queryClient.removeQueries({ queryKey: userQueryKey });
      onSuccess?.();
    },
  });
};

export const logout = (): Promise<void> => {
  return api.post('/auth/logout');
};

export const loginInputSchema = z.object({
  email: z.string().min(1, 'Required').email('Invalid email'),
  password: z.string().min(5, 'Required'),
});

export type LoginInput = z.infer<typeof loginInputSchema>;
const loginWithEmailAndPassword = (data: LoginInput): Promise<AuthResponse> => {
  return api.post('/auth/login', data);
};

export const registerInputSchema = z
  .object({

    email: z.string().min(1, 'Required'),
    username: z.string().min(1, 'Required'),
    full_name: z.string(),
    password: z
      .string()
      .min(6, 'Password must be at least 6 characters')
      .regex(/^(?=.*[A-Z])(?=.*\d).*/, 'Password must contain at least one uppercase letter and one digit'),
    confirmPassword: z
      .string()
      .min(6, 'Password must be at least 6 characters')
      .regex(/^(?=.*[A-Z])(?=.*\d).*/, 'Password must contain at least one uppercase letter and one digit'),
    company: z.string(),
    designation: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  });

export type RegisterInput = z.infer<typeof registerInputSchema>;

const registerUser = (
  data: RegisterInput,
): Promise<AuthResponse> => {
  return api.post('/auth/register', data);
};

// // File: lib/auth.ts
// import axiosInstance from "./axios";
// import {
//   LoginCredentials,
//   UserRegistration,
//   User,
//   AuthTokens,
//   AuthResponse,
// } from "../types/auth";

// class AuthService {
//   private accessTokenKey = "access_token";
//   private refreshTokenKey = "refresh_token";
//   private accessToken: string | null = null;

//   constructor() {
//     if (typeof window !== "undefined") {
//       const storedToken = localStorage.getItem(this.accessTokenKey);
//       if (storedToken) {
//         this.accessToken = storedToken;
//       }
//     }

//     // Bind methods to preserve 'this' context
//     this.login = this.login.bind(this);
//     this.register = this.register.bind(this);
//     this.logout = this.logout.bind(this);
//     // this.getCurrentUser = this.getCurrentUser.bind(this);
//     this.refreshToken = this.refreshToken.bind(this);
//     this.setTokens = this.setTokens.bind(this);
//     this.clearTokens = this.clearTokens.bind(this);
//     // this.getAccessToken = this.getAccessToken.bind(this);
//     // this.isAuthenticated = this.isAuthenticated.bind(this);
//     // this.hasValidToken = this.hasValidToken.bind(this);
//   }

//   // hasValidToken(): boolean {
//   //   if (typeof window === "undefined") return false;
//   //   const token = localStorage.getItem(this.accessTokenKey);
//   //   return !!token;
//   // }

//   // async isAuthenticated(): Promise<boolean> {
//   //   if (typeof window === "undefined") return false;

//   //   try {
//   //     const user = await this.getCurrentUser();
//   //     return !!user; // Will return true if user data exists
//   //   } catch {
//   //     this.clearTokens();
//   //     return false;
//   //   }
//   // }


//   // getAccessToken(): string | null {
//   //   if (typeof window === "undefined") return null;
//   //   return this.accessToken || localStorage.getItem(this.accessTokenKey);
//   // }

//   setTokens(tokens: AuthTokens): void {
//     if (typeof window === "undefined") {
//       console.log("[AuthService] setTokens skipped: window undefined");
//       return;
//     }

//     this.accessToken = tokens.accessToken;
//     localStorage.setItem(this.accessTokenKey, tokens.accessToken);

//     if (tokens.refreshToken) {
//       localStorage.setItem(this.refreshTokenKey, tokens.refreshToken);
//       console.log(
//         "[AuthService] setTokens: refreshToken stored",
//         tokens.refreshToken
//       );
//     }
//   }

//   clearTokens(): void {
//     if (typeof window === "undefined") return;
//     this.accessToken = null;
//     localStorage.removeItem(this.accessTokenKey);
//     localStorage.removeItem(this.refreshTokenKey);
//   }

//   async login(credentials: LoginCredentials): Promise<AuthTokens> {
//     try {
//       const response = await axiosInstance.post("/auth/login", credentials);

//       // Adjust if your backend uses snake_case or camelCase here:
//       const tokens: AuthTokens = {
//         accessToken: response.data.accessToken || response.data.access_token,
//         refreshToken: response.data.refreshToken || response.data.refresh_token,
//       };

//       this.setTokens(tokens);

//       return { ...tokens };
//     } catch (error: any) {
//       console.error("[AuthService] login error", error);
//       throw new Error(error.response?.data?.message || "Login failed");
//     }
//   }

//   async register(userData: UserRegistration): Promise<AuthResponse> {
//     try {
//       const response = await axiosInstance.post("/auth/register", userData);
//       return response.data;
//     } catch (error: any) {
//       throw new Error(error.response?.data?.message || "Registration failed");
//     }
//   }

//   // async getCurrentUser(): Promise<User> {
//   //   try {
//   //     const response = await axiosInstance.get("/users/me");
//   //     console.log("🚀 ~ AuthService ~ getCurrentUser ~ response:", response)
//   //     return response.data;
//   //   } catch (error: any) {
//   //     throw new Error(
//   //       error.response?.data?.message || "Failed to get user data"
//   //     );
//   //   }
//   // }

//   async refreshToken(): Promise<string> {
//     try {
//       const response = await axiosInstance.post("/auth/refresh", null, {
//         withCredentials: true,
//       });

//       const newAccessToken =
//         response.data.accessToken || response.data.access_token;

//       this.setTokens({
//         accessToken: newAccessToken,
//       });

//       return newAccessToken;
//     } catch (error: any) {
//       this.clearTokens();
//       throw new Error(error.response?.data?.message || "Token refresh failed");
//     }
//   }

//   // async ensureAccessToken(): Promise<string | null> {
//   //   if (!this.hasValidToken()) {
//   //     try {
//   //       const newToken = await this.refreshToken();
//   //       return newToken;
//   //     } catch {
//   //       this.clearTokens();
//   //       return null;
//   //     }
//   //   }
//   //   return this.getAccessToken();
//   // }

//   async logout(): Promise<void> {
//     try {
//       await axiosInstance.post("/auth/logout");
//     } catch (error) {
//       console.error("Logout API call failed:", error);
//     } finally {
//       this.clearTokens();
//     }
//   }
// }

// export default new AuthService();
