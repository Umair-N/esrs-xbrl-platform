'use client';

import { useState } from 'react';
import { AdminSidebar } from '@/components/admin/admin-sidebar';
import { DashboardHeader } from '@/components/admin/dashboard-header';
import { OverviewCards } from '@/components/admin/overview-cards';
import { AnalyticsCharts } from '@/components/admin/analytics-charts';
import { UserManagement } from '@/components/admin/user-management';
import { CustomWidgets } from '@/components/admin/custom-widgets';
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar';

export default function AdminDashboard() {
  const [activeView, setActiveView] = useState('overview');

  // const renderContent = () => {
  //   switch (activeView) {
  //     case 'overview':
  //       return (
  //         <div className='space-y-6'>
  //           <OverviewCards />
  //           <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
  //             <AnalyticsCharts />
  //             <CustomWidgets />
  //           </div>
  //         </div>
  //       );
  //     case 'users':
  //       return <UserManagement />;
  //     case 'analytics':
  //       return (
  //         <div className='space-y-6'>
  //           <AnalyticsCharts />
  //           <CustomWidgets />
  //         </div>
  //       );
  //     default:
  //       return (
  //         <div className='space-y-6'>
  //           <OverviewCards />
  //           <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
  //             <AnalyticsCharts />
  //             <CustomWidgets />
  //           </div>
  //         </div>
  //       );
  //   }
  // };

  return (
    <SidebarProvider>
      <AdminSidebar activeView={activeView} setActiveView={setActiveView} />
      <SidebarInset>
        <DashboardHeader />
        <main className='flex-1 space-y-4 p-4 md:p-8 pt-6'>
          {/* {renderContent()} */}
          <div className='space-y-6'>
            <OverviewCards />
            <div className='grid grid-cols-1 lg:grid-cols-2 gap-6'>
              <AnalyticsCharts />
              <CustomWidgets />
            </div>
          </div>
        </main>
      </SidebarInset>
    </SidebarProvider>
  );
}
