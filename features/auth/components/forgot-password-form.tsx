'use client';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from '@/components/ui/form';
import { Mail, ArrowLeft } from 'lucide-react';
import type { UseFormReturn } from 'react-hook-form';
import type * as z from 'zod';
import type { forgotPasswordInputSchema } from '@/lib/auth';
import { showSuccess } from '@/components/heads-up';
import Link from 'next/link';

type ForgotPasswordSchema = z.infer<typeof forgotPasswordInputSchema>;

interface ForgotPasswordFormProps {
  forgotPasswordForm: UseFormReturn<ForgotPasswordSchema>;
}

export function ForgotPasswordForm({
  forgotPasswordForm,
}: ForgotPasswordFormProps) {
  const onSubmit = async (values: ForgotPasswordSchema) => {
    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1000));
      console.log('[v0] Forgot password form submitted:', values);
      showSuccess({ title: 'Password reset link sent to your email!' });
      forgotPasswordForm.reset();
    } catch (error) {
      console.error('[v0] Forgot password error:', error);
    }
  };

  return (
    <Form {...forgotPasswordForm}>
      <form
        onSubmit={forgotPasswordForm.handleSubmit(onSubmit)}
        className="space-y-6"
      >
        <div className="text-center mb-6">
          <p className="text-gray-400 text-sm">
            Enter your email address and we'll send you a link to reset your
            password.
          </p>
        </div>

        <FormField
          control={forgotPasswordForm.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormControl>
                <div className="relative">
                  <Mail className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                  <Input
                    {...field}
                    type="email"
                    placeholder="Enter your email"
                    className="h-12 pl-12 bg-gray-800/30 border-gray-600/50 text-white placeholder:text-gray-500 rounded-xl focus:border-purple-500 focus:ring-purple-500/20"
                  />
                </div>
              </FormControl>
              <FormMessage className="text-red-400 text-sm" />
            </FormItem>
          )}
        />

        <Button
          type="submit"
          disabled={forgotPasswordForm.formState.isSubmitting}
          className="w-full h-12 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white font-medium rounded-xl transition-all duration-200 shadow-lg hover:shadow-purple-500/25"
        >
          {forgotPasswordForm.formState.isSubmitting
            ? 'Sending...'
            : 'Send Reset Link'}
        </Button>

        <div className="text-center">
          <Link
            href="?page=login"
            className="inline-flex items-center gap-2 text-sm text-gray-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Sign In
          </Link>
        </div>
      </form>
    </Form>
  );
}
