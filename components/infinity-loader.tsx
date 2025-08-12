'use client';

interface InfinityLoaderProps {
  text?: string;
  className?: string;
}

export default function InfinityLoader({
  text = 'Loading...',
  className = '',
}: InfinityLoaderProps) {
  return (
    <div
      className={`fixed inset-0 bg-gray-900 flex items-center justify-center z-50 ${className}`}
    >
      <div className='flex flex-col items-center space-y-8'>
        {/* Infinity Symbol */}
        <div className='relative'>
          <svg
            width='80'
            height='40'
            viewBox='0 0 80 40'
            className='animate-spin'
            style={{ animationDuration: '2s' }}
          >
            <defs>
              <linearGradient
                id='infinityGradient'
                x1='0%'
                y1='0%'
                x2='100%'
                y2='0%'
              >
                <stop offset='0%' stopColor='#3b82f6' />
                <stop offset='50%' stopColor='#06b6d4' />
                <stop offset='100%' stopColor='#10b981' />
              </linearGradient>
            </defs>
            <path
              d='M20 20 C20 10, 10 10, 10 20 C10 30, 20 30, 20 20 C20 10, 30 10, 30 20 C30 30, 40 30, 40 20 C40 10, 50 10, 50 20 C50 30, 60 30, 60 20 C60 10, 70 10, 70 20 C70 30, 60 30, 60 20'
              fill='none'
              stroke='url(#infinityGradient)'
              strokeWidth='4'
              strokeLinecap='round'
              strokeLinejoin='round'
            />
          </svg>
        </div>

        {/* Loading Text */}
        {text && (
          <p className='text-white/70 text-lg font-medium tracking-wide'>
            {text}
          </p>
        )}

        {/* Pulsing Dots */}
        <div className='flex space-x-2'>
          <div
            className='w-2 h-2 bg-blue-400 rounded-full animate-pulse'
            style={{ animationDelay: '0ms' }}
          ></div>
          <div
            className='w-2 h-2 bg-cyan-400 rounded-full animate-pulse'
            style={{ animationDelay: '200ms' }}
          ></div>
          <div
            className='w-2 h-2 bg-emerald-400 rounded-full animate-pulse'
            style={{ animationDelay: '400ms' }}
          ></div>
        </div>
      </div>
    </div>
  );
}
