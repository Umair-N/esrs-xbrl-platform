'use client';

import { useEffect, useMemo } from 'react';
import { useRouter, usePathname, useSearchParams } from 'next/navigation';

type NavigateProps = {
  to: string;
  replace?: boolean;
  // mimic React Router state; we serialize as query params
  state?: Record<string, string | number | boolean | null | undefined>;
};

function buildUrl(to: string, state?: NavigateProps['state']) {
  if (!state || Object.keys(state).length === 0) return to;
  const url = new URL(to, 'http://localhost'); // base ignored
  const sp = new URLSearchParams(url.search);
  for (const [k, v] of Object.entries(state)) {
    if (v === undefined) continue;
    // stringify non-strings
    sp.set(k, typeof v === 'string' ? v : JSON.stringify(v));
  }
  url.search = sp.toString();
  return url.pathname + (url.search ? `?${url.search}` : '');
}

export default function Navigate({ to, replace, state }: NavigateProps) {
  const router = useRouter();
  const pathname = usePathname();
  const search = useSearchParams();

  // if user passed { from: location } like in React Router examples:
  const computedState = useMemo(() => {
    if (state && 'from' in state && (state as any).from === 'location') {
      // allow a shorthand where from: "location" means current path+query
      const current =
        pathname + (search.toString() ? `?${search.toString()}` : '');
      return { ...state, from: current };
    }
    return state;
  }, [pathname, search, state]);

  useEffect(() => {
    const url = buildUrl(to, computedState);
    if (replace) router.replace(url);
    else router.push(url);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [to, replace, computedState, router]);

  return null;
}
