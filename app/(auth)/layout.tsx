'use client';

import Navigate from '@/components/navigate';
import PageSwitcherLoader from '@/components/page-switcher-loader';
import { useUser } from '@/lib/auth';

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { status, data: user, isLoading } = useUser();
  if (isLoading) return <PageSwitcherLoader />;

  return status === 'success' ? <Navigate to='/' /> : children;
}
