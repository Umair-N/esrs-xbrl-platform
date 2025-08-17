import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  BriefcaseIcon,
  BuildingIcon,
  LockIcon,
  MailIcon,
  UserIcon,
} from 'lucide-react';
import * as z from 'zod';
import { registerInputSchema, useRegister } from '@/lib/auth';
import { showError, showSuccess } from '@/components/heads-up';
import { useRouter } from 'next/navigation';

type RegisterSchema = z.infer<typeof registerInputSchema>;

export function RegisterForm({ registerForm }: { registerForm: any }) {
  const params = new URLSearchParams(window.location.search);
  const router = useRouter();
  const registerMutation = useRegister({
    onSuccess: async () => {
      showSuccess({ title: 'Registration successful! Please sign in.' });
      params.set('page', 'login');
      router.push(`?${params.toString()}`);
      registerForm.reset();
    },
    onError: (err) => {
      showError({ title: (err as Error).message || 'Registration failed' });
    },
  });

  const onRegisterSubmit = async (values: RegisterSchema) => {
    const { ...registrationData } = values;
    registerMutation.mutate(registrationData);
  };
  return (
    <>
      <Form {...registerForm}>
        <form
          onSubmit={registerForm.handleSubmit(onRegisterSubmit)}
          className="space-y-4"
          key="signup-form" // Add key to force re-render
        >
          <div className="grid grid-cols-2 gap-4">
            <FormField
              control={registerForm.control}
              name="full_name"
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <div className="relative">
                      <UserIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                      <Input
                        placeholder="Full name"
                        {...field}
                        className="bg-gray-800/50 border-gray-600/50 text-white placeholder:text-gray-400 focus:border-purple-500 focus:ring-purple-500/20 h-12 rounded-xl pl-11"
                      />
                    </div>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={registerForm.control}
              name="username"
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <div className="relative">
                      <UserIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                      <Input
                        placeholder="Username"
                        {...field}
                        className="bg-gray-800/50 border-gray-600/50 text-white placeholder:text-gray-400 focus:border-purple-500 focus:ring-purple-500/20 h-12 rounded-xl pl-11"
                      />
                    </div>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>

          <FormField
            control={registerForm.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormControl>
                  <div className="relative">
                    <MailIcon className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <Input
                      type="email"
                      placeholder="Enter your email"
                      {...field}
                      className="bg-gray-800/50 border-gray-600/50 text-white placeholder:text-gray-400 focus:border-purple-500 focus:ring-purple-500/20 h-12 rounded-xl pl-12"
                    />
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <div className="grid grid-cols-2 gap-4">
            <FormField
              control={registerForm.control}
              name="company"
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <div className="relative">
                      <BuildingIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                      <Input
                        placeholder="Company"
                        {...field}
                        className="bg-gray-800/50 border-gray-600/50 text-white placeholder:text-gray-400 focus:border-purple-500 focus:ring-purple-500/20 h-12 rounded-xl pl-11"
                      />
                    </div>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={registerForm.control}
              name="designation"
              render={({ field }) => (
                <FormItem>
                  <FormControl>
                    <div className="relative">
                      <BriefcaseIcon className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                      <Input
                        placeholder="Job title"
                        {...field}
                        className="bg-gray-800/50 border-gray-600/50 text-white placeholder:text-gray-400 focus:border-purple-500 focus:ring-purple-500/20 h-12 rounded-xl pl-11"
                      />
                    </div>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>

          <FormField
            control={registerForm.control}
            name="password"
            render={({ field }) => (
              <FormItem>
                <FormControl>
                  <div className="relative">
                    <LockIcon className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <Input
                      type="password"
                      placeholder="Create password"
                      {...field}
                      className="bg-gray-800/50 border-gray-600/50 text-white placeholder:text-gray-400 focus:border-purple-500 focus:ring-purple-500/20 h-12 rounded-xl pl-12"
                    />
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={registerForm.control}
            name="confirmPassword"
            render={({ field }) => (
              <FormItem>
                <FormControl>
                  <div className="relative">
                    <LockIcon className="absolute right-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <Input
                      type="password"
                      placeholder="Confirm password"
                      {...field}
                      className="bg-gray-800/50 border-gray-600/50 text-white placeholder:text-gray-400 focus:border-purple-500 focus:ring-purple-500/20 h-12 rounded-xl pl-12"
                    />
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <Button
            type="submit"
            className="w-full h-12 bg-gradient-to-r from-purple-600 to-purple-700 hover:from-purple-700 hover:to-purple-800 text-white font-semibold rounded-xl shadow-lg hover:shadow-purple-500/25 transition-all duration-200 mt-6"
            disabled={registerMutation.isPending}
          >
            {registerMutation.isPending ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2" />
                Creating account...
              </div>
            ) : (
              'Create an account'
            )}
          </Button>
        </form>
      </Form>
    </>
  );
}
