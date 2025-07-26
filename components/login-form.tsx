import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";

import { useAuth } from "../hooks/useAuth";
import {
  Form, FormControl, FormField, FormItem, FormLabel, FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { MailIcon, LockIcon, AlertTriangle } from "lucide-react";

const loginSchema = z.object({
  email: z.string().email({ message: "Invalid email address" }),
  password: z.string().min(6, { message: "Password must be at least 6 characters" }),
});

type LoginSchema = z.infer<typeof loginSchema>;

const LoginForm = () => {
  const { login, isAuthenticated, loading: authLoading } = useAuth();
  const router = useRouter();

  const [error, setError] = useState<string | null>(null);
  const [formLoading, setFormLoading] = useState(false);
  const [isRedirecting, setIsRedirecting] = useState(false);

  const form = useForm<LoginSchema>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onSubmit = async (values: LoginSchema) => {
    console.log('Login attempt started');
    setError(null);
    setFormLoading(true);
    
    try {
      await login(values);
      console.log('Login successful, redirecting immediately');
      
      // Show loading state briefly, then redirect
      setIsRedirecting(true);
      
      // Immediate redirect to avoid hot reload interference
      setTimeout(() => {
        window.location.href = "/";
      }, 500);
      
    } catch (err) {
      console.error('Login failed:', err);
      setError((err as Error).message || "Login failed");
      setIsRedirecting(false);
    } finally {
      setFormLoading(false);
    }
  };

  // Debug logging
  useEffect(() => {
    console.log('Auth state:', { isAuthenticated, authLoading, isRedirecting });
  }, [isAuthenticated, authLoading, isRedirecting]);

  return (
    <div className="max-w-md mx-auto mt-10 p-6 rounded-lg shadow-sm border bg-white relative">
      <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>

      {/* Redirecting loader overlay - less intrusive */}
      {isRedirecting && (
        <div className="absolute inset-0 bg-white/70 flex items-center justify-center z-40 rounded-lg">
          <div className="text-center bg-white p-4 rounded-lg shadow-lg border">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-2"></div>
            <p className="text-sm text-gray-700 font-medium">Redirecting...</p>
          </div>
        </div>
      )}

      {error && (
        <Alert variant="destructive" className="mb-4">
          <AlertTriangle className="h-4 w-4" />
          <AlertTitle>Error</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
          {/* Email */}
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <div className="relative">
                    <MailIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                    <Input
                      type="email"
                      placeholder="you@example.com"
                      {...field}
                      className="pl-10"
                    />
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          {/* Password */}
          <FormField
            control={form.control}
            name="password"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Password</FormLabel>
                <FormControl>
                  <div className="relative">
                    <LockIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                    <Input
                      type="password"
                      placeholder="••••••••"
                      {...field}
                      className="pl-10"
                    />
                  </div>
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <Button type="submit" className="w-full" disabled={formLoading || authLoading || isRedirecting}>
            {isRedirecting ? "Redirecting..." : formLoading ? "Logging in..." : "Login"}
          </Button>
        </form>
      </Form>

      <p className="mt-4 text-center text-sm text-muted-foreground">
        Don&apos;t have an account?{" "}
        <a href="/register" className="text-blue-600 hover:underline">
          Sign up
        </a>
      </p>
    </div>
  );
};

export default LoginForm;