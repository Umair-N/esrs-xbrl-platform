'use client';

import { useState, useEffect } from 'react';

interface LoadingScreenProps {
  onComplete?: () => void;
  duration?: number;
}

export default function XbrlLoader() {
  const [progress, setProgress] = useState(0);
  const [currentMessage, setCurrentMessage] = useState(0);

  const messages = [
    'Initializing AI reporting engine...',
    'Processing XBRL taxonomies...',
    'Preparing intelligent insights...',
    'Optimizing financial data analysis...',
  ];

  useEffect(() => {
    const progressInterval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(progressInterval);
          //   setTimeout(() => onComplete?.(), 500)
          return 100;
        }
        return prev + 100 / (2000 / 100);
      });
    }, 100);

    const messageInterval = setInterval(() => {
      setCurrentMessage((prev) => (prev + 1) % messages.length);
    }, 1500);

    return () => {
      clearInterval(progressInterval);
      clearInterval(messageInterval);
    };
  }, []);

  return (
    <div className='fixed inset-0 z-50 flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-50'>
      {/* Floating background elements - more professional/data-themed */}
      <div className='absolute inset-0 overflow-hidden'>
        <div
          className='absolute top-1/4 left-1/4 w-32 h-32 rounded-lg bg-blue-100 opacity-20 float-animation rotate-12'
          style={{ animationDelay: '0s' }}
        />
        <div
          className='absolute top-3/4 right-1/4 w-24 h-24 rounded-lg bg-indigo-100 opacity-30 float-animation -rotate-12'
          style={{ animationDelay: '1s' }}
        />
        <div
          className='absolute top-1/2 left-3/4 w-20 h-20 rounded-lg bg-slate-200 opacity-25 float-animation rotate-45'
          style={{ animationDelay: '2s' }}
        />
        {/* Additional data visualization elements */}
        <div
          className='absolute top-1/3 right-1/3 w-16 h-16 border-2 border-blue-200 rounded-full opacity-20 float-animation'
          style={{ animationDelay: '0.5s' }}
        />
      </div>

      {/* Main loading content */}
      <div className='relative z-10 text-center space-y-8 px-8'>
        {/* Logo/Brand area - more professional for XBRL platform */}
        <div className='space-y-4'>
          <div className='w-20 h-20 mx-auto rounded-2xl gradient-shift pulse-glow flex items-center justify-center bg-gradient-to-br from-blue-600 to-indigo-600'>
            <div className='flex items-center space-x-1'>
              <div className='w-3 h-3 bg-white rounded-full opacity-90' />
              <div className='w-2 h-6 bg-white rounded-sm opacity-90' />
              <div className='w-3 h-4 bg-white rounded-sm opacity-90' />
            </div>
          </div>
          <div className='space-y-2'>
            <h1 className='text-3xl font-bold text-slate-800'>
              XBRL AI Platform
            </h1>
            <p className='text-sm text-slate-500 font-medium'>
              Intelligent Financial Reporting
            </p>
          </div>
        </div>

        {/* Animated message */}
        <div className='h-8 flex items-center justify-center'>
          <p
            key={currentMessage}
            className='text-lg text-slate-600 animate-in fade-in duration-500 font-medium'
          >
            {messages[currentMessage]}
          </p>
        </div>

        {/* Progress indicator */}
        <div className='space-y-4 w-80 max-w-full'>
          {/* Progress bar */}
          <div className='relative'>
            <div className='w-full h-3 bg-slate-200 rounded-full overflow-hidden'>
              <div
                className='h-full bg-gradient-to-r from-blue-600 to-indigo-600 transition-all duration-300 ease-out rounded-full relative overflow-hidden'
                style={{ width: `${progress}%` }}
              >
                <div className='absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer' />
              </div>
            </div>
            <div className='mt-3 text-sm text-slate-500 font-semibold'>
              {Math.round(progress)}% Complete
            </div>
          </div>

          <div className='flex justify-center space-x-2'>
            <div className='w-3 h-3 rounded-full bounce-dot-1 bg-blue-600' />
            <div className='w-3 h-3 rounded-full bounce-dot-2 bg-indigo-600' />
            <div className='w-3 h-3 rounded-full bounce-dot-3 bg-slate-600' />
          </div>
        </div>

        <div className='text-xs text-slate-400 max-w-sm mx-auto'>
          <p className='animate-pulse'>
            Leveraging AI to streamline your regulatory reporting workflow...
          </p>
        </div>
      </div>
    </div>
  );
}
