import { useRouter } from 'next/router';
import { useEffect } from 'react';

export default function OverviewPage() {
  const router = useRouter();

  useEffect(() => {
    router.push('/admin');
  }, [router]);
}
