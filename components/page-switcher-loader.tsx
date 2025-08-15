'use client';

import { useState, useEffect } from 'react';

interface PageSwitcherLoadingProps {
  message?: string;
}

export default function PageSwitcherLoader({
  message = 'Loading...',
}: PageSwitcherLoadingProps) {
  //   useEffect(() => {
  //     const interval = setInterval(() => {
  //       setDots((prev) => {
  //         if (prev === '...') return '';
  //         return prev + '.';
  //       });
  //     }, 400);

  //     return () => clearInterval(interval);
  //   }, []);

  return (
    <div className='fixed inset-0 z-40 bg-white/80 backdrop-blur-sm flex items-center justify-center'>
      {/* Subtle background pattern */}
      <div className='absolute inset-0 opacity-5'>
        <div className='absolute top-1/4 left-1/4 w-16 h-16 border border-blue-200 rounded-lg rotate-45 animate-spin-slow' />
        <div className='absolute bottom-1/4 right-1/4 w-12 h-12 border border-indigo-200 rounded-full animate-pulse' />
      </div>

      {/* Loading content */}
      <div className='relative z-10 text-center space-y-6'>
        {/* Compact logo */}
        <div className='w-12 h-12 mx-auto rounded-xl bg-gradient-to-br from-blue-600 to-indigo-600 flex items-center justify-center animate-pulse'>
          <div className='flex items-center space-x-0.5'>
            <div className='w-1.5 h-1.5 bg-white rounded-full opacity-90' />
            <div className='w-1 h-3 bg-white rounded-sm opacity-90' />
            <div className='w-1.5 h-2 bg-white rounded-sm opacity-90' />
          </div>
        </div>

        {/* Loading message */}
        <div className='space-y-2'>
          <p className='text-lg font-semibold text-slate-700'>{message}</p>
          <div className='flex justify-center items-center space-x-1'>
            <div
              className='w-2 h-2 bg-blue-600 rounded-full animate-bounce'
              style={{ animationDelay: '0ms' }}
            />
            <div
              className='w-2 h-2 bg-indigo-600 rounded-full animate-bounce'
              style={{ animationDelay: '150ms' }}
            />
            <div
              className='w-2 h-2 bg-slate-600 rounded-full animate-bounce'
              style={{ animationDelay: '300ms' }}
            />
          </div>
        </div>

        {/* Progress bar - indeterminate */}
        <div className='w-48 h-1 bg-slate-200 rounded-full overflow-hidden'>
          <div className='h-full bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full animate-progress-slide' />
        </div>
      </div>
    </div>
  );
}
