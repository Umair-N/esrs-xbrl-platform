// // File: hooks/useAuthQueries.ts
// import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
// import { useRouter } from "next/navigation";
// // import AuthService from "../lib/auth";
// import { LoginCredentials, UserRegistration, User } from "../types/auth";
// import { MutationConfig } from "@/lib/react-query";
// import { api } from "@/lib/api-client";
// import { logout, registerInputSchema } from "@/lib/auth";

// // Query Keys
// export const authKeys = {
//   all: ["auth"] as const,
//   user: () => [...authKeys.all, "user"] as const,
//   currentUser: () => [...authKeys.user(), "current"] as const,
// };

// // Get Current User Query
// export const useCurrentUser = () => {
//   return useQuery({
//     queryKey: authKeys.currentUser(),
//     queryFn: () => api.get("/users/me"),
//     // enabled: AuthService.hasValidToken(),
//     retry: false,
//     refetchOnWindowFocus: false,
//   });
// };

// // Login Mutation
// export const useLogin = (
//   config: MutationConfig<typeof AuthService.login> = {}
// ) => {
//   const queryClient = useQueryClient();

//   return useMutation({
//     mutationFn: AuthService.login,
//     onSuccess: async (data, variables) => {
//       // Set user data immediately if returned from login
//       if (data.user) {
//         queryClient.setQueryData(authKeys.currentUser(), data.user);
//       }

//       // Invalidate and refetch user data to ensure sync
//       await queryClient.invalidateQueries({ queryKey: authKeys.user() });

//       // If no user data returned, fetch it
//       if (!data.user) {
//         try {
//           const userData = await queryClient.fetchQuery({
//             queryKey: authKeys.currentUser(),
//             queryFn: () => api.get("/users/me"),
//             staleTime: 0, // Force fresh fetch
//           });
//           queryClient.setQueryData(authKeys.currentUser(), userData);
//         } catch (error) {
//           console.error("Failed to fetch user after login:", error);
//         }
//       }

//       // Call custom onSuccess if provided
//       config.onSuccess?.(data, variables, undefined);
//     },
//     onError: (error, variables, context) => {
//       // Call custom onError if provided
//       config.onError?.(error, variables, context);
//     },
//     ...config,
//   });
// };

// // Register Mutation
// export const useRegister = (
//   config: MutationConfig<typeof registerInputSchema> = {}
// ) => {
//   return useMutation({
//     mutationFn: register,
//     ...config,
//   });
// };

// // Logout Mutation
// export const useLogout = (
//   config: MutationConfig<typeof logout> = {}
// ) => {
//   const queryClient = useQueryClient();
//   const router = useRouter();

//   return useMutation({
//     mutationFn: logout,
//     onSuccess: (data, variables, context) => {
//       // Clear all auth-related queries
//       queryClient.removeQueries({ queryKey: authKeys.all });

//       // Clear user data
//       queryClient.setQueryData(authKeys.currentUser(), null);

//       // Reset query cache completely for auth
//       queryClient.clear();

//       // Redirect to login
//       router.push("/login");

//       // Call custom onSuccess if provided
//       config.onSuccess?.(data, variables, context);
//     },
//     ...config,
//   });
// };

// // Check if user is authenticated (derived from query state)
// export const useIsAuthenticated = () => {
//   const { data: user, isLoading, isError } = useCurrentUser();

//   return {
//     isAuthenticated: !!user && !isError,
//     isLoading,
//     user,
//   };
// };
