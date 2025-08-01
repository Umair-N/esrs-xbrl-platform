"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";
import { useAuth } from "@/hooks/useAuth";
import Spinner from "@/components/spinner";

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // Only redirect if we're certain the user is not authenticated
    if (!loading && !isAuthenticated) {
      router.replace("/login");
    }
  }, [loading, isAuthenticated, router]);

  // Show loading only while auth state is being determined
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center flex-col gap-2">
        <Spinner />
        <p className="text-sm text-gray-500">Loading...</p>
      </div>
    );
  }

  // If not authenticated after loading, don't render children
  // The useEffect will handle the redirect
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center flex-col gap-2">
        <Spinner />
        <p className="text-sm text-gray-500">Redirecting...</p>
      </div>
    );
  }

  // Only render the main layout when authenticated
  return (
    <div className="flex flex-col min-h-screen">
      <SiteHeader />
      <main className="flex-1">{children}</main>
      <SiteFooter />
    </div>
  );
}