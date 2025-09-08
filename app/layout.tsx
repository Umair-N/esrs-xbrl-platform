'use client';
import './globals.css';
import { Inter } from 'next/font/google';
import { Toaster } from '@/components/ui/sonner';
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from '@/lib/react-query';
import { Metadata } from 'next';
import {
  NotificationContainer,
  NotificationProvider,
} from '@/components/heads-up';

const inter = Inter({ subsets: ['latin'] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const isProduction = process.env.NODE_ENV === 'production';

  return (
    <html lang='en'>
      <head>
        {isProduction && (
          <meta
            httpEquiv='Content-Security-Policy'
            content='upgrade-insecure-requests'
          />
        )}
      </head>
      <link rel='icon' href='/favicon.png' sizes='any' />
      <body className={inter.className}>
        <NotificationProvider>
          <NotificationContainer />
          <QueryClientProvider client={queryClient}>
            <Toaster richColors position='top-right' closeButton />
            <div className='relative flex min-h-screen flex-col'>
              {children}
            </div>
          </QueryClientProvider>
        </NotificationProvider>
      </body>
    </html>
  );
}
