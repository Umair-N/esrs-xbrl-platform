'use client';
import { useUser } from '@/lib/auth';
import Navigate from '@/components/navigate';

export function AdminAccess({
  children,
  showError,
}: {
  children: React.ReactNode;
  showError?: boolean;
}) {
  const { data: user } = useUser();

  return user?.role?.toLocaleLowerCase() === 'admin' ? (
    <>{children}</>
  ) : showError ? (
    <Navigate to='/unauthorized' />
  ) : null;
}
