'use client';

import { useEffect } from 'react';
import { Button } from '@/components/ui/button';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className='min-h-screen bg-gradient-to-br from-amber-50 to-yellow-50 flex items-center justify-center p-4'>
      <div className='max-w-md w-full text-center space-y-8'>
        {/* Error Icon */}
        <div className='relative'>
          <div className='w-32 h-32 mx-auto bg-amber-600 rounded-full flex items-center justify-center'>
            <svg
              className='w-16 h-16 text-white'
              fill='none'
              stroke='currentColor'
              viewBox='0 0 24 24'
            >
              <path
                strokeLinecap='round'
                strokeLinejoin='round'
                strokeWidth={2}
                d='M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z'
              />
            </svg>
          </div>
          <div className='absolute -top-2 -right-2 w-8 h-8 bg-red-500 rounded-full flex items-center justify-center'>
            <span className='text-white text-sm font-bold'>!</span>
          </div>
        </div>

        {/* Content */}
        <div className='space-y-4'>
          <h2 className='text-2xl font-bold text-amber-800'>
            Something Went Wrong
          </h2>
          <p className='text-amber-700 leading-relaxed'>
            An unexpected error occurred while processing your request. Our team
            has been notified and is working to fix this issue.
          </p>
          {error.digest && (
            <p className='text-xs text-amber-600 font-mono bg-amber-100 px-3 py-2 rounded'>
              Error ID: {error.digest}
            </p>
          )}
        </div>

        {/* Actions */}
        <div className='flex flex-col sm:flex-row gap-3 justify-center'>
          <Button onClick={reset} className='bg-amber-600 hover:bg-amber-700'>
            Try Again
          </Button>
          <Button
            variant='outline'
            onClick={() => (window.location.href = '/')}
            className='border-amber-200 text-amber-700 hover:bg-amber-50'
          >
            Go Home
          </Button>
        </div>

        {/* Decorative Elements */}
        <div className='absolute top-20 left-10 w-2 h-2 bg-amber-200 rounded-full opacity-60'></div>
        <div className='absolute top-32 right-16 w-1 h-1 bg-amber-300 rounded-full opacity-40'></div>
        <div className='absolute bottom-40 left-20 w-1.5 h-1.5 bg-amber-200 rounded-full opacity-50'></div>
      </div>
    </div>
  );
}
