'use client';

import InfinityLoader from '@/components/infinity-loader';
import Navigate from '@/components/navigate';
import { useUser } from '@/lib/auth';

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { status, data: user, isLoading } = useUser();
  if (isLoading) return <InfinityLoader />;

  return status === 'success' ? <Navigate to='/' /> : children;
}
