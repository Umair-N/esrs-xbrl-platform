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

// export const metadata: Metadata = {
//   title: 'ESRS XBRL Tagging Platform',
//   description:
//     'A comprehensive solution for tagging financial reports with ESRS XBRL concepts',
// };

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang='en'>
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
