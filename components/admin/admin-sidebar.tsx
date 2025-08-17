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
import { usePathname } from 'next/navigation';
import Link from 'next/link';

const navigationItems = [
  {
    title: 'Overview',
    icon: Home,
    href: 'overview',
  },
  {
    title: 'User Management',
    icon: Users,
    href: '/admin/users',
  },
  // {
  //   title: 'Analytics',
  //   icon: BarChart3,
  //   href: '/admin/analytics',
  // },
  // {
  //   title: 'Activity Monitor',
  //   icon: Activity,
  //   href: '/admin/activity',
  // },
  // {
  //   title: 'Data Management',
  //   icon: Database,
  //   href: '/admin/data',
  // },
];

const adminItems = [
  // {
  //   title: 'Security',
  //   icon: Shield,
  //   href: '/admin/security',
  // },
  {
    title: 'Settings',
    icon: Settings,
    href: '/admin/settings',
  },
  // {
  //   title: 'Notifications',
  //   icon: Bell,
  //   href: '/admin/notifications',
  // },
];

export function AdminSidebar() {
  const pathname = usePathname();

  const isActive = (href: string) => {
    return pathname === href || pathname.startsWith(href + '/');
  };

  return (
    <Sidebar variant="inset">
      <SidebarHeader>
        <div className="flex items-center gap-2 px-4 py-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <BarChart3 className="h-4 w-4" />
          </div>
          <div className="grid flex-1 text-left text-sm leading-tight">
            <span className="truncate font-semibold">BriskBold AI</span>
            <span className="truncate text-xs text-muted-foreground">
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
                <SidebarMenuItem key={item.href}>
                  <SidebarMenuButton asChild isActive={isActive(item.href)}>
                    <Link href={item.href}>
                      <item.icon className="h-4 w-4" />
                      <span>{item.title}</span>
                    </Link>
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
                <SidebarMenuItem key={item.href}>
                  <SidebarMenuButton asChild isActive={isActive(item.href)}>
                    <Link href={item.href}>
                      <item.icon className="h-4 w-4" />
                      <span>{item.title}</span>
                    </Link>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <div className="p-4">
          <Button asChild variant="outline" className="w-full bg-transparent">
            <Link href="/admin/system-settings">
              <Settings className="h-4 w-4 mr-2" />
              System Settings
            </Link>
          </Button>
        </div>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
