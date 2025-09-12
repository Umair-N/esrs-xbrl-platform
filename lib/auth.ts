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
      localStorage.removeItem('xbrl-editor-session')
      localStorage.removeItem('xbrl-session-id')
      onSuccess?.();
    },
    onSettled: () => {
      localStorage.removeItem('xbrl-editor-session')
      localStorage.removeItem('xbrl-session-id')
    }
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

export const forgotPasswordInputSchema = z.object({
  email: z.string().email({ message: "Invalid email address" }),
})

export type ForgotPasswordInput = z.infer<typeof forgotPasswordInputSchema>
