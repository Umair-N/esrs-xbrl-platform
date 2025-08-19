'use client';

import { AdminSidebar } from '@/components/admin/admin-sidebar';
import { DashboardHeader } from '@/components/admin/dashboard-header';
import { OverviewCards } from '@/components/admin/overview-cards';
import { AnalyticsCharts } from '@/components/admin/analytics-charts';
// import { UserManagement } from '@/components/admin/user-management';
import { CustomWidgets } from '@/components/admin/custom-widgets';
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar';

export default function AdminDashboard() {
  return (
    <main className="flex-1 p-4 pt-6 space-y-4 md:p-8">
      {/* {renderContent()} */}
      <div className="space-y-6">
        <OverviewCards />
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          <AnalyticsCharts />
          <CustomWidgets />
        </div>
      </div>
    </main>
  );
}
