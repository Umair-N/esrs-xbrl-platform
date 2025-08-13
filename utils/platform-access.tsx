'use client';
import PlatformAccessError from '@/errors/platform-access';
import { useUser } from '@/lib/auth';

export function PlatformAccess({
  children,
  showError,
}: {
  children: React.ReactNode;
  showError?: boolean;
}) {
  const { data: user } = useUser();

  return user?.platform_access ? (
    <>{children}</>
  ) : showError ? (
    <PlatformAccessError />
  ) : null;
}
