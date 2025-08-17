'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { useRouter } from 'next/navigation';

export default function NotFound() {
  const router = useRouter();
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full text-center space-y-8">
        {/* 404 Number */}
        <div className="relative">
          <h1 className="text-9xl font-bold text-slate-200 select-none">404</h1>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-24 h-24 bg-slate-800 rounded-full flex items-center justify-center">
              <svg
                className="w-12 h-12 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.29-1.007-5.824-2.448M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                />
              </svg>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="space-y-4">
          <h2 className="text-2xl font-bold text-slate-800">Page Not Found</h2>
          <p className="text-slate-600 leading-relaxed">
            The page you're looking for doesn't exist. It might have been moved,
            deleted, or you entered the wrong URL.
          </p>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Button asChild className="bg-slate-800 hover:bg-slate-700">
            <Link href="/">Go Home</Link>
          </Button>
          <Button variant="outline" onClick={() => router.back()}>
            Go Back
          </Button>
        </div>

        {/* Decorative Elements */}
        <div className="absolute top-20 left-10 w-2 h-2 bg-slate-300 rounded-full opacity-60"></div>
        <div className="absolute top-32 right-16 w-1 h-1 bg-slate-400 rounded-full opacity-40"></div>
        <div className="absolute bottom-40 left-20 w-1.5 h-1.5 bg-slate-300 rounded-full opacity-50"></div>
      </div>
    </div>
  );
}
