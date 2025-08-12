import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function Unauthorized() {
  return (
    <div className='min-h-screen bg-gradient-to-br from-red-50 to-orange-50 flex items-center justify-center p-4'>
      <div className='max-w-md w-full text-center space-y-8'>
        {/* 401 Number */}
        <div className='relative'>
          <h1 className='text-9xl font-bold text-red-100 select-none'>401</h1>
          <div className='absolute inset-0 flex items-center justify-center'>
            <div className='w-24 h-24 bg-red-600 rounded-full flex items-center justify-center'>
              <svg
                className='w-12 h-12 text-white'
                fill='none'
                stroke='currentColor'
                viewBox='0 0 24 24'
              >
                <path
                  strokeLinecap='round'
                  strokeLinejoin='round'
                  strokeWidth={2}
                  d='M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z'
                />
              </svg>
            </div>
          </div>
        </div>

        {/* Content */}
        <div className='space-y-4'>
          <h2 className='text-2xl font-bold text-red-800'>Access Denied</h2>
          <p className='text-red-700 leading-relaxed'>
            You don't have permission to access this resource. Please sign in
            with the appropriate credentials or contact support.
          </p>
        </div>

        {/* Actions */}
        <div className='flex flex-col sm:flex-row gap-3 justify-center'>
          <Button asChild className='bg-red-600 hover:bg-red-700'>
            <Link href='/login'>Sign In</Link>
          </Button>
          <Button
            variant='outline'
            asChild
            className='border-red-200 text-red-700 hover:bg-red-50 bg-transparent'
          >
            <Link href='/'>Go Home</Link>
          </Button>
        </div>

        {/* Decorative Elements */}
        <div className='absolute top-20 left-10 w-2 h-2 bg-red-200 rounded-full opacity-60'></div>
        <div className='absolute top-32 right-16 w-1 h-1 bg-red-300 rounded-full opacity-40'></div>
        <div className='absolute bottom-40 left-20 w-1.5 h-1.5 bg-red-200 rounded-full opacity-50'></div>
      </div>
    </div>
  );
}
