"use client"
import Spinner from "@/components/spinner";
import { useIsAuthenticated } from "@/hooks/useAuthQueries";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isAuthenticated, isLoading } = useIsAuthenticated();
  const router = useRouter();

  useEffect(() => {
    // Only redirect if we're certain the user is authenticated
    if (!isLoading && isAuthenticated) {
      router.replace("/dashboard"); // or wherever you want to redirect after login
    }
  }, [isLoading, isAuthenticated, router]);

  // Show loading while auth state is being determined
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center flex-col gap-2">
        <Spinner />
        <p className="text-sm text-gray-500">Loading...</p>
      </div>
    );
  }

  // If authenticated after loading, don't render auth forms
  // The useEffect will handle the redirect
  if (isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center flex-col gap-2">
        <Spinner />
        <p className="text-sm text-gray-500">Redirecting...</p>
      </div>
    );
  }

  // Only render auth forms when not authenticated
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      {children}
    </div>
  );
}

