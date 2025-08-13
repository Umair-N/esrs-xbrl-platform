'use client';

import {
  BarChart3,
  Users,
  Settings,
  Shield,
  Bell,
  Home,
  Activity,
  Database,
} from 'lucide-react';
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from '@/components/ui/sidebar';
import { Button } from '@/components/ui/button';

const navigationItems = [
  {
    title: 'Overview',
    icon: Home,
    id: 'overview',
  },
  {
    title: 'User Management',
    icon: Users,
    id: 'users',
  },
  {
    title: 'Analytics',
    icon: BarChart3,
    id: 'analytics',
  },
  {
    title: 'Activity Monitor',
    icon: Activity,
    id: 'activity',
  },
  {
    title: 'Data Management',
    icon: Database,
    id: 'data',
  },
];

const adminItems = [
  {
    title: 'Security',
    icon: Shield,
    id: 'security',
  },
  {
    title: 'Settings',
    icon: Settings,
    id: 'settings',
  },
  {
    title: 'Notifications',
    icon: Bell,
    id: 'notifications',
  },
];

interface AdminSidebarProps {
  activeView: string;
  setActiveView: (view: string) => void;
}

export function AdminSidebar({ activeView, setActiveView }: AdminSidebarProps) {
  return (
    <Sidebar variant='inset'>
      <SidebarHeader>
        <div className='flex items-center gap-2 px-4 py-2'>
          <div className='flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground'>
            <BarChart3 className='h-4 w-4' />
          </div>
          <div className='grid flex-1 text-left text-sm leading-tight'>
            <span className='truncate font-semibold'>BriskBold AI</span>
            <span className='truncate text-xs text-muted-foreground'>
              Dashboard
            </span>
          </div>
        </div>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Main Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {navigationItems.map((item) => (
                <SidebarMenuItem key={item.id}>
                  <SidebarMenuButton
                    isActive={activeView === item.id}
                    onClick={() => setActiveView(item.id)}
                  >
                    <item.icon className='h-4 w-4' />
                    <span>{item.title}</span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
        <SidebarGroup>
          <SidebarGroupLabel>Administration</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {adminItems.map((item) => (
                <SidebarMenuItem key={item.id}>
                  <SidebarMenuButton
                    isActive={activeView === item.id}
                    onClick={() => setActiveView(item.id)}
                  >
                    <item.icon className='h-4 w-4' />
                    <span>{item.title}</span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <div className='p-4'>
          <Button variant='outline' className='w-full bg-transparent'>
            <Settings className='h-4 w-4 mr-2' />
            System Settings
          </Button>
        </div>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
