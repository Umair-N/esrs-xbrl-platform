'use client';
import { useState } from 'react';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { MailIcon, Eye, EyeOff } from 'lucide-react';
import { loginInputSchema, useLogin } from '@/lib/auth';
import { showError, showSuccess } from '@/components/heads-up';
import { useRouter } from 'next/navigation';
import * as z from 'zod';
import Link from 'next/link';

export function LoginForm({ loginForm }: any) {
  const router = useRouter();
  const [showPassword, setShowPassword] = useState(false);

  const loginMutation = useLogin({
    onSuccess: async () => {
      showSuccess({ title: 'Login successful', message: 'Welcome back!' });
      router.push('/');
    },
    onError: (err) => {
      showError({ title: (err as Error).message || 'Login failed' });
    },
  });
  type LoginSchema = z.infer<typeof loginInputSchema>;

  const onLoginSubmit = async (values: LoginSchema) => {
    try {
      loginMutation.mutate(values);
    } catch (error) {
      console.error('Login submission error:', error);
    }
  };

  return (
    <Form {...loginForm}>
      <form
        onSubmit={loginForm.handleSubmit(onLoginSubmit)}
        className='space-y-4'
        key='signin-form' // Add key to force re-render
      >
        <FormField
          control={loginForm.control}
          name='email'
          render={({ field }) => (
            <FormItem>
              <FormControl>
                <div className='relative'>
                  <MailIcon className='absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5' />
                  <Input
                    type='email'
                    placeholder='Enter your email'
                    {...field}
                    id='email'
                    autoComplete='email'
                    className='bg-gray-800/50 border-gray-600/50 text-white placeholder:text-gray-400 focus:border-purple-500 focus:ring-purple-500/20 h-12 rounded-xl pl-12'
                  />
                </div>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={loginForm.control}
          name='password'
          render={({ field }) => (
            <FormItem>
              <FormControl>
                <div className='relative'>
                  <button
                    type='button'
                    onClick={() => setShowPassword(!showPassword)}
                    className='absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400  transition-colors z-10'
                  >
                    {showPassword ? (
                      <EyeOff className='w-5 h-5' />
                    ) : (
                      <Eye className='w-5 h-5' />
                    )}
                  </button>
                  <Input
                    type={showPassword ? 'text' : 'password'}
                    placeholder='Enter your password'
                    {...field}
                    id='password'
                    className='bg-gray-800/50 border-gray-600/50 text-white placeholder:text-gray-400 focus:border-purple-500 focus:ring-purple-500/20 h-12 rounded-xl pl-12 pr-12'
                  />
                </div>
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <div className='text-right'>
          <Link
            href='?page=forgot-password'
            className='text-sm text-purple-400 hover:text-purple-300 transition-colors'
          >
            Forgot password?
          </Link>
        </div>{' '}
        <Button
          type='submit'
          className='w-full h-12 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white font-semibold rounded-xl shadow-lg hover:shadow-purple-500/25 transition-all duration-200 mt-6'
          disabled={loginMutation.isPending}
        >
          {loginMutation.isPending ? (
            <div className='flex items-center justify-center'>
              <div className='animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2' />
              Signing in...
            </div>
          ) : (
            'Sign in'
          )}
        </Button>
      </form>
    </Form>
  );
}
