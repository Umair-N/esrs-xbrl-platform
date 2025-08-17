'use client';

import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import type * as z from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

import {
  loginInputSchema,
  registerInputSchema,
  forgotPasswordInputSchema,
} from '@/lib/auth';
import { RegisterForm } from '@/features/auth/components/register-form';
import { ForgotPasswordForm } from '@/features/auth/components/forgot-password-form';
import { LoginForm } from '@/features/auth/components/login-form';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { X } from 'lucide-react';

type LoginSchema = z.infer<typeof loginInputSchema>;
type RegisterSchema = z.infer<typeof registerInputSchema>;
type ForgotPasswordSchema = z.infer<typeof forgotPasswordInputSchema>;

interface AuthFormProps {
  onClose?: () => void;
}

const AuthForm = ({ onClose }: AuthFormProps) => {
  const searchParams = useSearchParams();
  const currentPage = searchParams.get('page');
  const isSignUp = currentPage === 'register';
  const isForgotPassword = currentPage === 'forgot-password';

  const loginForm = useForm<LoginSchema>({
    resolver: zodResolver(loginInputSchema),
    defaultValues: {
      email: '',
      password: '',
    },
  });

  const registerForm = useForm<RegisterSchema>({
    resolver: zodResolver(registerInputSchema),
    defaultValues: {
      email: '',
      username: '',
      full_name: '',
      password: '',
      confirmPassword: '',
      company: '',
      designation: '',
    },
  });

  const forgotPasswordForm = useForm<ForgotPasswordSchema>({
    resolver: zodResolver(forgotPasswordInputSchema),
    defaultValues: {
      email: '',
    },
  });

  useEffect(() => {
    if (isSignUp) {
      loginForm.reset();
      forgotPasswordForm.reset();
    } else if (isForgotPassword) {
      loginForm.reset();
      registerForm.reset();
    } else {
      registerForm.reset();
      forgotPasswordForm.reset();
    }
  }, [isSignUp, isForgotPassword, loginForm, registerForm, forgotPasswordForm]);

  const handleModeSwitch = () => {
    loginForm.clearErrors();
    registerForm.clearErrors();
    forgotPasswordForm.clearErrors();
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-gradient-to-br from-black via-gray-900 to-purple-900 relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-black/50 via-transparent to-purple-900/50" />

      <div className="relative w-full max-w-md">
        <div className="bg-gray-900/40 backdrop-blur-xl border border-gray-700/50 rounded-2xl p-8 shadow-2xl">
          {onClose && (
            <button
              onClick={onClose}
              className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          )}

          {!isForgotPassword && (
            <div className="flex bg-gray-800/50 rounded-xl p-1 mb-8">
              <Link
                href={`?page=register`}
                onClick={() => handleModeSwitch()}
                className={`flex-1 text-center py-2 px-4 rounded-lg text-sm font-medium transition-all ${
                  isSignUp
                    ? 'bg-white text-black'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                Sign up
              </Link>
              <Link
                href={`?page=login`}
                onClick={() => handleModeSwitch()}
                className={`flex-1 text-center py-2 px-4 rounded-lg text-sm font-medium transition-all ${
                  !isSignUp
                    ? 'bg-white text-black'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                Sign in
              </Link>
            </div>
          )}

          <h2 className="text-2xl font-bold text-white mb-8 text-center">
            {isForgotPassword
              ? 'Reset Password'
              : isSignUp
                ? 'Create an account'
                : 'Welcome back'}
          </h2>

          {isForgotPassword ? (
            <ForgotPasswordForm forgotPasswordForm={forgotPasswordForm} />
          ) : isSignUp ? (
            <RegisterForm registerForm={registerForm} />
          ) : (
            <LoginForm loginForm={loginForm} />
          )}

          {/* Social Login */}
          {/* <div className='mt-6'>
            <div className='relative'>
              <div className='absolute inset-0 flex items-center'>
                <div className='w-full border-t border-gray-600/50' />
              </div>
              <div className='relative flex justify-center text-sm'>
                <span className='px-4 bg-gray-900/40 text-gray-400 uppercase tracking-wider text-xs'>
                  OR SIGN IN WITH
                </span>
              </div>
            </div>

            <div className='mt-6 grid grid-cols-2 gap-3'>
              <Button
                variant='outline'
                className='h-12 bg-gray-800/30 border-gray-600/50 text-white hover:bg-gray-700/50 rounded-xl'
              >
                <Chrome className='w-5 h-5' />
              </Button>
              <Button
                variant='outline'
                className='h-12 bg-gray-800/30 border-gray-600/50 text-white hover:bg-gray-700/50 rounded-xl'
              >
                <Apple className='w-5 h-5' />
              </Button>
            </div>
          </div> */}

          {!isForgotPassword && (
            <p className="mt-6 text-center text-xs text-gray-400">
              By {isSignUp ? 'creating an account' : 'signing in'}, you agree to
              our{' '}
              <a href="#" className="text-purple-400 hover:text-purple-300">
                Terms & Service
              </a>
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default AuthForm;
