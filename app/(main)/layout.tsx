'use client';
import { SiteHeader } from '@/components/site-header';
import { SiteFooter } from '@/components/site-footer';
import { useUser } from '@/lib/auth';
import Navigate from '@/components/navigate';
import PageSwitcherLoader from '@/components/page-switcher-loader';
import { BriskyAIBot } from '@/components/briskyai-bot';

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  // const { isAuthenticated, loading } = useAuth();
  // const router = useRouter();

  // useEffect(() => {
  //   // Only redirect if we're certain the user is not authenticated
  //   if (!loading && !isAuthenticated) {
  //     router.replace("/login");
  //   }
  // }, [loading, isAuthenticated, router]);

  // Only render the main layout when authenticated

  const { status, data: user, isLoading } = useUser();
  if (isLoading) return <PageSwitcherLoader />;

  //FIXME: from backend fix responses
  //   if (error) {
  //     if ((error as AxiosErrorResponse)?.response?.status === 401) {
  //       ('rendered');
  //     } else if (
  //       (error as AxiosErrorResponse)?.response?.data?.message ===
  //       'No node found with this id'
  //     ) {
  //       return <Navigate to='/select-profile' />;
  //     } else {
  //       return <div>Something went wrong</div>;
  //     }
  //   }

  return status === 'success' ? (
    <div className='flex flex-col min-h-screen'>
      <SiteHeader />
      <main className='flex-1'>{children}</main>
      <BriskyAIBot />
      {/* <SiteFooter /> */}
    </div>
  ) : (
    <Navigate to='/login' />
  );
}
