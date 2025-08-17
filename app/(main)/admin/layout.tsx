import { AdminSidebar } from '@/components/admin/admin-sidebar';
import { DashboardHeader } from '@/components/admin/dashboard-header';
import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar';
import { AdminAccess } from '@/utils/admin-access';

export default function EditorLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AdminAccess showError>
      <SidebarProvider>
        <AdminSidebar />
        <SidebarInset>
          <DashboardHeader />

          {children}
        </SidebarInset>
      </SidebarProvider>
    </AdminAccess>
  );
}
