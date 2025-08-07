// File: hooks/useAuth.tsx (Updated to work with React Query)
"use client";
import {
  useState,
  useEffect,
  useContext,
  createContext,
  ReactNode,
  FC,
} from "react";
import { useCurrentUser, useIsAuthenticated } from "./useAuthQueries";
import {
  User,
  LoginCredentials,
  UserRegistration,
  AuthContextType,
  AuthTokens,
  AuthResponse,
} from "../types/auth";

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: FC<AuthProviderProps> = ({ children }) => {
  // Use React Query hooks for auth state
  const { user, isAuthenticated, isLoading } = useIsAuthenticated();
  
  // Legacy methods for backward compatibility
  // These are now handled by React Query mutations in useAuthQueries
  const login = async (credentials: LoginCredentials): Promise<AuthTokens> => {
    throw new Error("Use useLogin mutation from useAuthQueries instead");
  };

  const register = async (userData: UserRegistration): Promise<AuthResponse> => {
    throw new Error("Use useRegister mutation from useAuthQueries instead");
  };

  const logout = async (): Promise<void> => {
    throw new Error("Use useLogout mutation from useAuthQueries instead");
  };

  const checkAuth = async (): Promise<void> => {
    // This is now handled automatically by React Query
    console.log("Auth check is handled automatically by React Query");
  };

  const value: AuthContextType = {
    user,
    loading: isLoading,
    isAuthenticated,
    login,
    register,
    logout,
    checkAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

