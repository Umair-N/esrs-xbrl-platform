import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function PlatformAccessError() {
  return (
    <div className='min-h-screen bg-gradient-to-br from-amber-50 to-orange-50 flex items-center justify-center p-4'>
      <div className='max-w-md w-full text-center space-y-8'>
        {/* 401 Number */}
        <div className='relative'>
          <h1 className='text-9xl font-bold text-red-100 select-none'>401</h1>
          <div className='absolute inset-0 flex items-center justify-center'>
            <div className='w-24 h-24 bg-amber-600 rounded-full flex items-center justify-center'>
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
          <h2 className='text-2xl font-bold text-amber-800'>
            Platform Access Denied
          </h2>
          <p className='text-amber-700 leading-relaxed'>
            You currently don&apos;t have access to the platform.You can contact
            the administrator to request access.
          </p>
        </div>

        {/* Actions */}
        <div className='flex flex-col sm:flex-row gap-3 justify-center'>
          <Button asChild className='bg-amber-600 hover:bg-amber-700'>
            <a href='mailto:contact@briskbold.ai'>Contact Us</a>
          </Button>
          <Button
            variant='outline'
            asChild
            className='border-red-200 text-amber-700 hover:bg-red-50 bg-transparent'
          >
            <Link href='/'>Go Home</Link>
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
