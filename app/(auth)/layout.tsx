"use client";
import Spinner from "@/components/spinner";
import { useIsAuthenticated } from "@/hooks/useAuthQueries";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isAuthenticated, isLoading: authLoading } = useIsAuthenticated();
  const router = useRouter();

  useEffect(() => {
    if (isAuthenticated && !authLoading) {
      console.log("User is authenticated, redirecting to home...");
      router.replace("/");
    }
  }, [isAuthenticated, authLoading, router]);

  // Show loading while auth state is being determined
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center flex-col gap-2">
        <Spinner />
        <p className="text-sm text-gray-500">Loading...</p>
      </div>
    );
  }

  if (isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Redirecting...</p>
        </div>
      </div>
    );
  }
  // Only render auth forms when not authenticated
  return <div>{children}</div>;
}
