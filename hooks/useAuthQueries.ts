// File: hooks/useAuthQueries.ts
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';
import AuthService from '../lib/auth';
import { LoginCredentials, UserRegistration, User } from '../types/auth';
import { MutationConfig } from '@/lib/react-query';

// Query Keys
export const authKeys = {
  all: ['auth'] as const,
  user: () => [...authKeys.all, 'user'] as const,
  currentUser: () => [...authKeys.user(), 'current'] as const,
};

// Get Current User Query
export const useCurrentUser = () => {
  return useQuery({
    queryKey: authKeys.currentUser(),
    queryFn: () => AuthService.getCurrentUser(),
    enabled: AuthService.hasValidToken(), // Only run if we have a token
    staleTime: 1000 * 60 * 5, // 5 minutes
    gcTime: 1000 * 60 * 10, // 10 minutes (previously cacheTime)
    retry: false,
  });
};

// Login Mutation
export const useLogin = (config: MutationConfig<typeof AuthService.login> = {}) => {
  const queryClient = useQueryClient();
  const router = useRouter();

  return useMutation({
    mutationFn: AuthService.login,
    onSuccess: async (data, variables) => {
      // Invalidate and refetch user data
      queryClient.invalidateQueries({ queryKey: authKeys.user() });
      
      // Optionally set user data immediately if returned from login
      if (data.user) {
        queryClient.setQueryData(authKeys.currentUser(), data.user);
      } else {
        // Fetch current user if not returned
        try {
          const userData = await AuthService.getCurrentUser();
          queryClient.setQueryData(authKeys.currentUser(), userData);
        } catch (error) {
          console.error('Failed to fetch user after login:', error);
        }
      }

      // Call custom onSuccess if provided
      config.onSuccess?.(data, variables, undefined);
    },
    onError: (error, variables, context) => {
      // Call custom onError if provided
      config.onError?.(error, variables, context);
    },
    ...config,
  });
};

// Register Mutation
export const useRegister = (config: MutationConfig<typeof AuthService.register> = {}) => {
  return useMutation({
    mutationFn: AuthService.register,
    ...config,
  });
};

// Logout Mutation
export const useLogout = (config: MutationConfig<typeof AuthService.logout> = {}) => {
  const queryClient = useQueryClient();
  const router = useRouter();

  return useMutation({
    mutationFn: AuthService.logout,
    onSuccess: (data, variables, context) => {
      // Clear all auth-related queries
      queryClient.removeQueries({ queryKey: authKeys.all });
      
      // Clear user data
      queryClient.setQueryData(authKeys.currentUser(), null);
      
      // Redirect to login
      router.push('/login');
      
      // Call custom onSuccess if provided
      config.onSuccess?.(data, variables, context);
    },
    ...config,
  });
};

// Check if user is authenticated (derived from query state)
export const useIsAuthenticated = () => {
  const { data: user, isLoading } = useCurrentUser();
  const hasToken = AuthService.hasValidToken();
  
  return {
    isAuthenticated: !!user && hasToken,
    isLoading,
    user,
  };
};