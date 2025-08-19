'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import {
  FileText,
  BookOpen,
  Calendar,
  FileCode,
  Menu,
  X,
  Sparkles,
  LogOut,
} from 'lucide-react';
import { Button, buttonVariants } from '@/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { cn, getInitials } from '@/lib/utils';
import { useState } from 'react';
import { useLogout, useUser } from '@/lib/auth';
import { AdminAccess } from '@/utils/admin-access';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
// import { useLogout } from '@/hooks/useAuthQueries';

const navigation = [
  { name: 'Dashboard', href: '/', exact: true },
  {
    name: 'Editor',
    href: '/editor',
    icon: FileText,
    platform_access_needed: true,
  },
  {
    name: 'Contexts',
    href: '/contexts',
    icon: Calendar,
    platform_access_needed: true,
  },
  {
    name: 'Taxonomy',
    href: '/taxonomy',
    icon: BookOpen,
    platform_access_needed: true,
  },
  {
    name: 'XBRL Preview',
    href: '/xbrl-preview',
    icon: FileCode,
    platform_access_needed: true,
  },
];

export function SiteHeader() {
  const router = useRouter();
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const logoutMutation = useLogout({
    onSuccess: () => {
      router.push('/login');
    },
  });
  const { data: user } = useUser();

  return (
    <header className="sticky top-0 z-50 w-full bg-white/80 dark:bg-slate-900/80 backdrop-blur-xl border-b border-slate-300 dark:border-slate-700/50">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-xl text-slate-900 dark:text-white">
              Brisk Bold
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  `flex items-center gap-2 text-sm font-medium transition-colors hover:text-blue-600 dark:hover:text-blue-400 ${
                    item.platform_access_needed
                      ? item.platform_access_needed === user?.platform_access
                        ? ''
                        : 'hidden'
                      : ''
                  }`,
                  (
                    item.exact
                      ? pathname === item.href
                      : pathname.startsWith(item.href)
                  )
                    ? 'text-blue-600 dark:text-blue-400'
                    : 'text-slate-600 dark:text-slate-400'
                )}
              >
                {item.icon && <item.icon className="h-4 w-4" />}
                {item.name}
              </Link>
            ))}
          </nav>

          {/* Right Side - Auth & Theme */}
          <div className="flex items-center gap-4">
            {/* Auth Section */}
            <AdminAccess>
              <Link
                href="/admin"
                className={`${buttonVariants(
                  {}
                )} bg-gradient-to-r from-blue-600 to-purple-600 flex items-center gap-2 text-sm font-medium hover:scale-95 hover:bg-gradient-to-br hover:from-blue-600 hover:to-purple-600 duration-200 transition-all`}
              >
                <Sparkles className="size-4" />
                Admin
              </Link>
            </AdminAccess>

            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <button className="relative rounded-full">
                  <Avatar className="size-10">
                    <AvatarImage
                    // src={`https://api.dicebear.com/7.x/initials/svg?seed=${user?.username}`}
                    />
                    <AvatarFallback className="text-lg font-medium bg-gradient-to-br from-blue-500 to-purple-600 text-white">
                      {getInitials(user?.full_name || user?.username)}
                    </AvatarFallback>
                  </Avatar>
                </button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end">
                <DropdownMenuLabel className="capitalize">
                  {user?.full_name || user?.username}
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                {/* <DropdownMenuItem>Profile</DropdownMenuItem>
                <DropdownMenuItem>Settings</DropdownMenuItem> */}
                {/* <DropdownMenuSeparator /> */}
                <DropdownMenuItem>
                  {' '}
                  <Button
                    onClick={() => logoutMutation.mutate()}
                    variant="ghost"
                    size="sm"
                    disabled={logoutMutation.isPending}
                    className="text-slate-600 hover:text-red-600 dark:text-slate-400 dark:hover:text-red-400 disabled:opacity-50 py-1 h-5"
                  >
                    <LogOut className="w-4 h-4 mr-2" />
                    <span className="hidden sm:inline">
                      {logoutMutation.isPending ? 'Signing Out...' : 'Sign Out'}
                    </span>
                  </Button>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
            {/* <span className="hidden sm:block text-sm font-medium text-slate-700 dark:text-slate-300">
              {user?.full_name || user?.username}
            </span> */}

            {/* Mobile Menu Trigger */}
            <Sheet open={open} onOpenChange={setOpen}>
              <SheetTrigger asChild>
                <Button variant="ghost" size="icon" className="md:hidden">
                  <Menu className="h-5 w-5" />
                  <span className="sr-only">Toggle menu</span>
                </Button>
              </SheetTrigger>
              <SheetContent side="left" className="pr-0">
                {/* <MobileNav
                  pathname={pathname}
                  setOpen={setOpen}
                  user={user}
                  isAuthenticated={isAuthenticated}
                  onLogout={handleLogout}
                  isLoggingOut={logoutMutation.isPending}
                /> */}
              </SheetContent>
            </Sheet>
          </div>
        </div>
      </div>
    </header>
  );
}

// function MobileNav({
//   pathname,
//   setOpen,
//   user,
//   isAuthenticated,
//   onLogout,
//   isLoggingOut,
// }: {
//   pathname: string;
//   setOpen: (open: boolean) => void;
//   user: any;
//   isAuthenticated: boolean;
//   onLogout: () => void;
//   isLoggingOut: boolean;
// }) {
//   const getInitials = (fullName?: string, username?: string): string => {
//     if (fullName) {
//       return fullName
//         .split(' ')
//         .map((n: string) => n[0])
//         .join('')
//         .toUpperCase();
//     }
//     return username?.slice(0, 2).toUpperCase() || 'U';
//   };

//   return (
//     <div className="flex flex-col h-full">
//       {/* Mobile Header */}
//       <div className="flex items-center justify-between p-4 border-b">
//         <Link
//           href="/"
//           className="flex items-center gap-3"
//           onClick={() => setOpen(false)}
//         >
//           <div className="w-6 h-6 bg-gradient-to-r from-blue-600 to-purple-600 rounded-md flex items-center justify-center">
//             <Sparkles className="w-4 h-4 text-white" />
//           </div>
//           <span className="font-bold text-lg">XBRL Platform</span>
//         </Link>
//         <Button variant="ghost" size="icon" onClick={() => setOpen(false)}>
//           <X className="h-5 w-5" />
//           <span className="sr-only">Close</span>
//         </Button>
//       </div>

//       {/* Mobile Navigation */}
//       <div className="flex-1 px-4 py-6">
//         <div className="flex flex-col space-y-2">
//           {navigation.map((item) => (
//             <Link
//               key={item.name}
//               href={item.href}
//               onClick={() => setOpen(false)}
//               className={cn(
//                 `flex items-center gap-3 rounded-lg px-3 py-3 text-sm font-medium transition-colors hover:bg-slate-100 dark:hover:bg-slate-800`,
//                 (
//                   item.exact
//                     ? pathname === item.href
//                     : pathname.startsWith(item.href)
//                 )
//                   ? 'bg-blue-50 dark:bg-blue-950/20 text-blue-600 dark:text-blue-400'
//                   : 'text-slate-600 dark:text-slate-400'
//               )}
//             >
//               {item.icon && <item.icon className="h-5 w-5" />}
//               {item.name}
//             </Link>
//           ))}
//         </div>
//       </div>

//       {/* Mobile Auth Section */}
//       <div className="border-t p-4">
//         {isAuthenticated ? (
//           <div className="space-y-4">
//             <div className="flex items-center gap-3 p-3 bg-slate-50 dark:bg-slate-800 rounded-lg">
//               <Avatar className="h-10 w-10">
//                 <AvatarImage
//                   src={`https://api.dicebear.com/7.x/initials/svg?seed=${user?.username}`}
//                 />
//                 <AvatarFallback className="text-sm bg-gradient-to-br from-blue-500 to-purple-600 text-white">
//                   {getInitials(user?.full_name, user?.username)}
//                 </AvatarFallback>
//               </Avatar>
//               <div className="flex-1 min-w-0">
//                 <p className="text-sm font-medium text-slate-900 dark:text-white truncate">
//                   {user?.full_name || user?.username}
//                 </p>
//                 <p className="text-xs text-slate-500 dark:text-slate-400 truncate">
//                   {user?.email}
//                 </p>
//               </div>
//             </div>
//             <Button
//               onClick={() => {
//                 onLogout();
//                 setOpen(false);
//               }}
//               variant="outline"
//               disabled={isLoggingOut}
//               className="w-full justify-start text-red-600 hover:text-red-700 hover:bg-red-50 dark:text-red-400 dark:hover:text-red-300 dark:hover:bg-red-950/20 disabled:opacity-50"
//             >
//               <LogOut className="w-4 h-4 mr-2" />
//               {isLoggingOut ? 'Signing Out...' : 'Sign Out'}
//             </Button>
//           </div>
//         ) : (
//           <div className="space-y-3">
//             <Button asChild variant="outline" className="w-full">
//               <Link href="/login" onClick={() => setOpen(false)}>
//                 Sign In
//               </Link>
//             </Button>
//             <Button
//               asChild
//               className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
//             >
//               <Link href="/register" onClick={() => setOpen(false)}>
//                 Get Started
//               </Link>
//             </Button>
//           </div>
//         )}
//       </div>
//     </div>
//   );
// }
