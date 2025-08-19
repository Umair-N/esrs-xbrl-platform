'use client';

import { Bell, Search } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Badge } from '@/components/ui/badge';
import { SidebarTrigger } from '@/components/ui/sidebar';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';

export function DashboardHeader() {
  return (
    <header className="flex h-16 shrink-0 items-center gap-2 border-b bg-gradient-to-r from-background to-muted/20 px-4">
      <SidebarTrigger className="-ml-1" />
      <div className="flex flex-1 items-center gap-2 px-3">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            type="search"
            placeholder="Search users, reports, or data..."
            className="pl-10 bg-background/50 border-border/50 focus:bg-background transition-colors"
          />
        </div>
        <div className="flex items-center gap-2 ml-auto">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                className="relative hover:bg-muted/50"
              >
                <Bell className="h-4 w-4" />
                <Badge className="absolute -top-1 -right-1 h-5 w-5 flex items-center justify-center p-0 text-xs bg-gradient-to-r from-red-500 to-red-600">
                  3
                </Badge>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-80">
              <DropdownMenuLabel>Notifications</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem className="p-3">
                <div className="flex flex-col gap-1">
                  <p className="text-sm font-medium">New user registration</p>
                  <p className="text-xs text-muted-foreground">
                    John Doe registered 5 minutes ago
                  </p>
                </div>
              </DropdownMenuItem>
              <DropdownMenuItem className="p-3">
                <div className="flex flex-col gap-1">
                  <p className="text-sm font-medium">Access request pending</p>
                  <p className="text-xs text-muted-foreground">
                    Jane Smith requested system access
                  </p>
                </div>
              </DropdownMenuItem>
              <DropdownMenuItem className="p-3">
                <div className="flex flex-col gap-1">
                  <p className="text-sm font-medium">User access revoked</p>
                  <p className="text-xs text-muted-foreground">
                    Access removed for inactive user
                  </p>
                </div>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </div>
    </header>
  );
}
