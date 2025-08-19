import { useUser } from '@/lib/auth';

export function hasPlatformAccess() {
  const { data: user } = useUser();
  return user?.platform_access;
}
