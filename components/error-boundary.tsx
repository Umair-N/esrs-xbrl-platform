'use client';

import React from 'react';

interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ComponentType<{ error: Error; reset: () => void }>;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends React.Component<
  ErrorBoundaryProps,
  ErrorBoundaryState
> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError && this.state.error) {
      const FallbackComponent = this.props.fallback;
      if (FallbackComponent) {
        return (
          <FallbackComponent
            error={this.state.error}
            reset={() => this.setState({ hasError: false, error: null })}
          />
        );
      }

      // Default fallback
      return (
        <div className='min-h-screen bg-gradient-to-br from-red-50 to-pink-50 flex items-center justify-center p-4'>
          <div className='max-w-md w-full text-center space-y-6'>
            <div className='w-24 h-24 mx-auto bg-red-600 rounded-full flex items-center justify-center'>
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
                  d='M6 18L18 6M6 6l12 12'
                />
              </svg>
            </div>
            <h2 className='text-2xl font-bold text-red-800'>
              Something went wrong
            </h2>
            <button
              onClick={() => this.setState({ hasError: false, error: null })}
              className='px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors'
            >
              Try again
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
